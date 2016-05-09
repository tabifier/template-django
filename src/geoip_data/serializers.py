from rest_framework import serializers


class CityGeoIPSerializer(serializers.Serializer):
    city = serializers.CharField(required=False)
    country_code = serializers.CharField(required=False)
    country_name = serializers.CharField(required=False)
    dma_code = serializers.IntegerField(required=False)
    latitude = serializers.DecimalField(required=False, max_digits=7, decimal_places=5)
    longitude = serializers.DecimalField(required=False, max_digits=7, decimal_places=5)
    postal_code = serializers.CharField(required=False)
    region = serializers.CharField(required=False)
