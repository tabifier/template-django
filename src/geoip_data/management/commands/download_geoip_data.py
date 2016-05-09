import os
import sys
import json
import logging
import requests
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Downloads the latest build of MaxMind GeoIP data if one does not already exists
    in the default file storage system (local, S3, etc...) as defined in settings.

    """

    def file_exists(self, file_path):
        gs_filename = "gs://{}/{}".format(settings.GEOIP_STORAGE_BUCKET_NAME, file_path)
        l = subprocess.Popen(
            [
                "gsutil",
                "ls",
                gs_filename
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = l.communicate()
        # if l.returncode:
        #     raise Exception('{} exit code on exists\n{}'.format(l.returncode, err))
        out = out.split('\n')
        return gs_filename in out

    def download(self, gs_path, local_path):
        gs_filename = "gs://{}/{}".format(settings.GEOIP_STORAGE_BUCKET_NAME, gs_path)
        l = subprocess.Popen(
            [
                "gsutil",
                "cp",
                gs_filename,
                local_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = l.communicate()
        if l.returncode:
            raise Exception('{} exit code on download\n{}'.format(l.returncode, err))

    def upload(self, local_path, gs_path):
        gs_filename = "gs://{}/{}".format(settings.GEOIP_STORAGE_BUCKET_NAME, gs_path)
        l = subprocess.Popen(
            [
                "gsutil",
                "cp",
                local_path,
                gs_filename,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = l.communicate()
        out, err = l.communicate()
        if l.returncode:
            raise Exception('{} exit code on upload\n{}'.format(l.returncode, err))

    def handle(self, *args, **options):
        geoip_md5_url = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.md5'
        geoip_data_url = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz'
        geoip_gzipped_data_file = 'geoip_data/data/GeoLite2-City.mmdb.gz'
        data_file_path = ''

        try:
            lastest_md5 = requests.get(geoip_md5_url).content
            data_file_path = 'geoip_data/data/GeoLite2-City.{}.mmdb.gz'.format(lastest_md5)

            if not self.file_exists(data_file_path):
                self.stdout.write(self.style.SUCCESS('Downloading MaxMind GeoIP2 city from: {}'.format(geoip_data_url)))
                with open(os.path.join(settings.BASE_DIR, data_file_path), 'w') as f:
                    response = requests.get(geoip_data_url, stream=True)
                    if not response.ok:
                        response = json.dumps({
                            'geoip_data_url': geoip_data_url,
                            'geoip_md5_url': geoip_md5_url,
                            'status_code': response.status_code,
                        }, indent=2)
                        raise Exception("GeoIP download error: Received and error while downloading MaxMind GeoIP2 database, {}".format(response))

                    try:
                        for block in response.iter_content(1024):
                            f.write(block)
                    except Exception, ex:
                        raise ex

                self.upload(os.path.join(settings.BASE_DIR, data_file_path), data_file_path)
                self.stdout.write(self.style.SUCCESS('Successfully downloaded MaxMind GeoIP2 city data'))

            self.stdout.write(self.style.SUCCESS('Getting a local copy of MaxMind GeoIP2 city data'))
            self.download(data_file_path, os.path.join(settings.BASE_DIR, geoip_gzipped_data_file))

            self.stdout.write(self.style.SUCCESS('Extracting city data'))
            subprocess.call(['gunzip', '-f', os.path.join(settings.BASE_DIR, geoip_gzipped_data_file)])

        except Exception, ex:
            # cleanup files on failure
            subprocess.call(['rm', '-rf', data_file_path])
            subprocess.call(['rm', '-rf', geoip_gzipped_data_file])

            logger.error('GeoIP download error: general exception received', exc_info=True)
            self.stdout.write(self.style.ERROR('Received and error while downloading MaxMind GeoIP2 database'))
            self.stdout.write(self.style.ERROR(ex))
            sys.exit(1)
