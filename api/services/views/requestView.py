from django.db import IntegrityError

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ..models import (
    ServiceProvider, ServiceRequest
)
from ..serializers.serializer_models import (
    ServiceProviderSerializer, RequestedServiceSerializer
)
from ..serializers.serializer_forms import (
    CreateServiceProviderSerilizer, ServiceRequestCreationSerializer
)
from ..crud.requestsCrud import (get_services_requests, get_service_providers)


class RequestPagination(PageNumberPagination):
    page_size = 5


# Service Provider CRUD Endpoint

class ServiceProviderView(APIView, RequestPagination):
    ProviderID = openapi.Parameter('ProviderID', openapi.IN_QUERY, description="Get by ProviderID param(optional)",
                                   type=openapi.TYPE_INTEGER)
    ProductID = openapi.Parameter('ProductID', openapi.IN_QUERY, description="Get by ProductID param(optional)",
                                  type=openapi.TYPE_INTEGER)
    LocationID = openapi.Parameter('LocationID', openapi.IN_QUERY, description="Get by LocationID param(optional)",
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        operation_description="Endpoint for getting Service Providers response [you may pass all the query params]",
        manual_parameters=[ProviderID, ProductID, LocationID],
        responses={200: openapi.Response(
            description='paginated Services Providers', schema=ServiceProviderSerializer(many=True)
        )}, paginator=RequestPagination())
    def get(self, request):
        data = request.query_params
        providers = get_service_providers(data)
        providers = self.paginate_queryset(providers, request, view=self)

        serializer = RequestedServiceSerializer(providers, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(operation_description="Endpoint for Service Providers Creation",
                         request_body=CreateServiceProviderSerilizer,
                         responses={200: ServiceProviderSerializer(many=False)}
                         )
    def post(self, request):

        data = request.data
        serializer = CreateServiceProviderSerilizer(data=data)
        if serializer.is_valid():
            provider = ServiceProvider(UserID_id=data["UserID"], ProductID_id=data["ProductID"],
                                       LocationID_id=data["LocationID"])
            if data["GenderID"] is not None:
                provider.GenderID_id = data["GenderID"]
            if data["AgeBracket"] is not None:
                provider.AgeBracket = data["AgeBracket"]
            try:
                provider.save()
                serializer = ServiceProviderSerializer(provider, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"Error": ["Db UserID or ProductID or LocationID or GenderID IntegrityError constraint failed"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Services CRUD Endpoint

class RequestServiceView(APIView, RequestPagination):
    UserID = openapi.Parameter('UserID', openapi.IN_QUERY, description="Get by UserID param(optional)",
                               type=openapi.TYPE_INTEGER)
    ProductID = openapi.Parameter('ProductID', openapi.IN_QUERY, description="Get by ProductID param(optional)",
                                  type=openapi.TYPE_INTEGER)
    LocationID = openapi.Parameter('LocationID', openapi.IN_QUERY, description="Get by LocationID param(optional)",
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Endpoint for Services Requests",
                         manual_parameters=[UserID, ProductID, LocationID],
                         responses={200: openapi.Response(
                             description='paginated Services Requests', schema=RequestedServiceSerializer(many=True)
                         )}, paginator=RequestPagination())
    def get(self, request):

        data = request.query_params
        requests = get_services_requests(data)
        requests = self.paginate_queryset(requests, request, view=self)

        serializer = RequestedServiceSerializer(requests, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=ServiceRequestCreationSerializer, responses={201: RequestedServiceSerializer(many=False)}
    )
    def post(self, request):
        data = request.data
        serializer = ServiceRequest(data=data)
        if serializer.is_valid():
            requests = ServiceRequest(
                ProductID_id=data["ProductID"], UserID_id=data["UserID"], LocationID_id=data["LocationID"]
            )
            if data["RequestText"] is not None:
                requests.RequestText = data["RequestText"]
            try:
                requests.save()
                serializer = RequestedServiceSerializer(requests, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"Error": ["Db ProductID or UserID or LocationID IntegrityError constraint failed"]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
