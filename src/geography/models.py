from __future__ import unicode_literals

from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    currency_code = models.CharField(max_length=3, null=True, blank=True)
    currency_name = models.CharField(max_length=50, null=True, blank=True)
    dial_code = models.CharField(max_length=8, null=True, blank=True)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return u"%s" % self.name


class Province(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    country = models.ForeignKey('Country')

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return u"{}, {}".format(self.name, self.country_id)
