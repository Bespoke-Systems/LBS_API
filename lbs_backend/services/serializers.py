from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import (
    WorkingDays, ServiceCategory, Service, Advertisement
)

from users.serializers import UserModelSerializer
from locations.serializers import CountyModelSerializers


class WorkingDaySerializer(ModelSerializer):
    class Meta:
        model = WorkingDays
        fields = ["days"]


class ServiceCategorySerailizer(ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = "__all__"


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "Name", "CategoryID"]


class InverseServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "Name"]


class InverseCategorySerializer(ModelSerializer):
    services = InverseServiceSerializer(source="category", many=True, read_only=True)

    class Meta:
        model = ServiceCategory
        fields = ["id", "Name", "services"]


class AdvertisementSerializer(ModelSerializer):
    from provider.serializers import ProviderSerializer
    Provider = ProviderSerializer(source="UserID", read_only=True, many=False)
    Location = CountyModelSerializers(source="LocationID", read_only=True, many=False)
    Service = InverseServiceSerializer(source="ServiceID", read_only=True, many=False)

    class Meta:
        model = Advertisement
        fields = [
            "id", "ADTitle", "Provider", "Service", "Location", "AdDescription", "StartDate", "ExpiryDate",
            "NoOfMessages"
        ]


class CreateAdvertSerializer(Serializer):
    ADTitle = serializers.CharField()
    UserID = serializers.IntegerField()
    ServiceID = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
    LocationID = serializers.IntegerField()
    AdDescription = serializers.CharField(allow_blank=True)
    StartDate = serializers.DateField(allow_null=True)
    ExpiryDate = serializers.DateField()
