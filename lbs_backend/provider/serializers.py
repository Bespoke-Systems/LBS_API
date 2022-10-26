from abc import ABC

from rest_framework import serializers
from .models import ProviderModel, ProviderService, ServiceResponse, ServiceRequest
from users.serializers import UserModelSerializer
from locations.serializers import CenterLocationSerializer, CountyModelSerializers


class ProviderSerializer(serializers.ModelSerializer):
    User = UserModelSerializer(read_only=True, source="UserID", many=False)
    County = CountyModelSerializers(source="CountyID", read_only=True, many=False)

    class Meta:
        model = ProviderModel
        fields = [
            "id", "User", "County"
        ]


class CreateProviderSerializer(serializers.Serializer):
    CountyID = serializers.IntegerField()


class ProviderServiceSerializer(serializers.ModelSerializer):
    from services.serializers import ServiceSerializer
    Provider = ProviderSerializer(read_only=True, source="ProviderID")
    Service = ServiceSerializer(read_only=True, source="ProductID")
    Location = CenterLocationSerializer(source="CenterLocationID", read_only=True)

    class Meta:
        model = ProviderService
        fields = [
            "id", "Provider", "ServiceTitle", "Service", "ServiceDescription", "Longitude", "Lattitude",
            "Location", "workingDays", "AgeBracket",
        ]


class CreatePostProviderServiceSerializer(serializers.Serializer):
    ServiceTitle = serializers.CharField()
    ProductID = serializers.IntegerField()
    ServiceDescription = serializers.CharField(allow_null=True, allow_blank=True)
    Longitude = serializers.CharField(max_length=50)
    Lattitude = serializers.CharField(max_length=50)
    CenterLocationID = serializers.IntegerField()


class SearchCenterLocationSerializer(serializers.Serializer):
    Longitude = serializers.CharField(max_length=50)
    Lattitude = serializers.CharField(max_length=50)


class UserStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    User = UserModelSerializer(many=False)
    Location = CountyModelSerializers(many=False)
    Provider = serializers.BooleanField()


class ServiceRequestSerializer(serializers.ModelSerializer):
    User = UserModelSerializer(read_only=True, source="UserID", many=False)
    Service = ProviderServiceSerializer(source="ProviderServiceID", many=False)
    CenterLocation = CenterLocationSerializer(source="CenterLocationID", many=False)

    class Meta:
        model = ServiceRequest
        fields = [
            "id", "User", "Service", "CenterLocation", "TimeStamp", "RequestText", "Latitude", "Longitude"
        ]


class ServiceResponseSerializer(serializers.ModelSerializer):
    Request = ServiceRequestSerializer(source="ServiceRequestID", many=False)

    class Meta:
        model = ServiceResponse
        fields = [
            "id", "Request", "ResponseText", "TimeStamp"
        ]


class CreateServiceRequestSerializer(serializers.Serializer):
    ProviderServiceID = serializers.IntegerField()
    RequestText = serializers.CharField(allow_blank=True, allow_null=True)
    CenterLocationID = serializers.IntegerField(allow_null=True)
    Latitude = serializers.CharField(allow_blank=True, allow_null=True)
    Longitude = serializers.CharField(allow_blank=True, allow_null=True)


class CreateServiceResponseSerializer(serializers.Serializer):
    ServiceRequestID = serializers.IntegerField()
    ResponseText = serializers.CharField(allow_blank=True, allow_null=True)


class SearchServiceSerializer(serializers.Serializer):
    searchdata = serializers.CharField()
    ServiceCategory = serializers.CharField(allow_blank=True)
    Region = serializers.CharField(allow_blank=True)
