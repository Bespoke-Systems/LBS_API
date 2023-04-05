from rest_framework import serializers
from rest_framework.serializers import Serializer

gender_choices = [
    (1, "Male"), (2, "Female")
]
age_bracket = [
    ('18+', '18+'), ('All', 'All'), ('10+', '10+'), ('16+', '16+'),
]


class CreateServiceProviderSerilizer(Serializer):
    UserID = serializers.IntegerField()
    ProductID = serializers.IntegerField()
    LocationID = serializers.IntegerField()
    GenderID = serializers.ChoiceField(choices=gender_choices)
    AgeBracket = serializers.ChoiceField(choices=age_bracket, default="All")


class ServiceRequestCreationSerializer(Serializer):
    UserID = serializers.IntegerField()
    ProductID = serializers.IntegerField()
    LocationID = serializers.IntegerField()
    RequestText = serializers.CharField(default="", allow_blank=True)


class ServiceResponseCreationSerializer(Serializer):
    RequestID = serializers.IntegerField()
    ProviderID = serializers.IntegerField()
    ResponseText = serializers.CharField(default="", allow_blank=True)
