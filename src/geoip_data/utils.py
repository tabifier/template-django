from django.contrib.gis.geoip2 import GeoIP2

_geo = GeoIP2()


def geoIP(ip_address, bubble_exceptions=False):
    try:
        return _geo.city(ip_address)
    except Exception, ex:
        if bubble_exceptions:
            raise ex
        return {
            "city": None,
            "country_code": None,
            "country_name": None,
            "dma_code": None,
            "latitude": None,
            "longitude": None,
            "postal_code": None,
            "region": None,
        }
