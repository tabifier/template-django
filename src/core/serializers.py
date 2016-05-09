from rest_framework import serializers

class ErrorSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    detail = serializers.CharField(required=True)
    source = serializers.CharField(required=False)

class ErrorsSerializer(serializers.Serializer):
    errors = ErrorSerializer(many=True)
