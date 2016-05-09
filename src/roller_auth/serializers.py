from django.contrib.auth.models import User
from rest_framework import serializers

from geoip_data.serializers import CityGeoIPSerializer
from roller_auth.constants import AuthErrorMessages
from roller_auth.models import UserEmail, UserProfile

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, required=True)

    def validate_email(self, value):
        '''
        Check that the email that the user wants to signup for is available
        '''
        if UserEmail.objects.filter(email=value).exists():
            raise serializers.ValidationError(AuthErrorMessages.EMAIL_IN_USE)

        return value

class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    token_type = serializers.CharField(required=True)
    expires = serializers.CharField(required=True)
    scope = serializers.CharField(required=True)


class ServerResponseSerializer(serializers.Serializer):
    request_ip = serializers.CharField()
    geoip = CityGeoIPSerializer(required=False)
    host = serializers.CharField()
    uptime = serializers.CharField()
    commit = serializers.CharField(required=False)
    branch = serializers.CharField(required=False)

class LogoutResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    deactivated = serializers.BooleanField()


class UserProfileSerializer(serializers.ModelSerializer):
    profile_color = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'profile_color',
            'profile_picture',
            'phone_number',
        ]


class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source='username', read_only=True, required=False)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    password = serializers.CharField(required=False, write_only=True)
    profile = UserProfileSerializer(required=False)
    initials = serializers.CharField(source='get_initials', read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'is_active', 'email', 'first_name', 'last_name', 'full_name', 'initials', 'profile', 'password', )
        read_only_fields = ('uuid', 'is_active', )

    def is_valid(self):
        '''
        Check that the email that the user wants to signup for is available
        '''
        valid = super(UserSerializer, self).is_valid()

        if 'password' in self.validated_data:
            # The following 2 lines are disabled until I think about the differnt
            # security implications of exposing password_saving via the me API
            #
            # password_data = self.validated_data.pop('password')
            # self.instance.set_password(password_data)
            self.validated_data.pop('password')

        if valid and 'full_name' in self.initial_data:
            fullname = self.initial_data['full_name'].split()
            if fullname:
                self.validated_data['first_name'] = fullname[0]
                if len(fullname) > 1:
                    self.validated_data['last_name'] = u' '.join(fullname[1:])
            else:
                self.validated_data['first_name'] = u''
                self.validated_data['last_name'] = u''

            subSerializer = UserSerializer(data=self.validated_data)
            valid = valid and subSerializer.is_valid()
            self._errors.update(subSerializer.errors)

        return valid

    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            # we could do something here to save the changes to user's profile
            validated_data.pop('profile')
        super(UserSerializer, self).update(instance, validated_data)
