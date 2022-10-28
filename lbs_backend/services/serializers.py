from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from django.utils.timezone import localtime
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
    Provider = ProviderSerializer(source="ProviderID", read_only=True, many=False)
    Location = CountyModelSerializers(source="LocationID", read_only=True, many=False)
    Service = InverseServiceSerializer(source="ServiceID", read_only=True, many=True)

    class Meta:
        model = Advertisement
        fields = [
            "id", "ADTitle", "Provider", "Service", "Location", "AdDescription", "StartDate", "ExpiryDate",
            "NoOfMessages"
        ]

2
class CreateAdvertSerializer(Serializer):
    ADTitle = serializers.CharField()
<<<<<<< Updated upstream
    ProviderID = serializers.IntegerField()
=======
<<<<<<< HEAD
=======
    ProviderID = serializers.IntegerField()
>>>>>>> c2aff0757e981291333d0b0e9aec16180e857d21
>>>>>>> Stashed changes
    ServiceID = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
    LocationID = serializers.IntegerField()
    AdDescription = serializers.CharField(allow_blank=True)
    StartDate = serializers.CharField(allow_null=True, allow_blank=True)
    ExpiryDate = serializers.DateField()
