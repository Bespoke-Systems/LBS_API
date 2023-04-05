from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    CustomUser, Gender
)

UserModel = get_user_model()


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "MobileNumber", "IDNumber", "FirstName"
        ]

    @staticmethod
    def validate_MobileNumber(MobileNumber):
        if not MobileNumber:
            raise serializers.ValidationError("Please set MobileNumber")
        return MobileNumber

    @staticmethod
    def validate_IDNumber(IDNumber):
        if IDNumber is None:
            raise serializers.ValidationError("Please set IDNumber")
        return IDNumber


class userDetailsValidationSerializer(serializers.Serializer):
    MobileNumber = serializers.CharField(max_length=12,
                                         min_length=12, error_messages={'blank': 'invalid mobile number',
                                                                        'length': 'invalid mobile number'})
    IDNumber = serializers.IntegerField()
    FirstName = serializers.CharField(max_length=50)
    SurName = serializers.CharField(max_length=50)


class userPutDetailSerializer(serializers.Serializer):
    UserID = serializers.IntegerField()
    LocationID = serializers.IntegerField()
    GenderID = serializers.IntegerField()
    password = serializers.CharField(min_length=8)


class tokenSerializer(serializers.Serializer):
    auth_token = serializers.CharField()


class CreateAuthToken(serializers.Serializer):
    MobileNumber = serializers.CharField(max_length=12, min_length=10)
    password = serializers.CharField(min_length=4)


class LoginResponseSerializer(serializers.Serializer):
    MobileNumber = serializers.CharField()
    FirstName = serializers.CharField()
    Auth_token = serializers.CharField()
