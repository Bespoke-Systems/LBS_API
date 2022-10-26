from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    ServiceCategory, Service, Advertisement
)
from .serializers import (
    ServiceCategorySerailizer, ServiceSerializer, InverseCategorySerializer,
    AdvertisementSerializer, CreateAdvertSerializer
)
from provider.models import ServiceResponse, ServiceRequest, ProviderModel
from provider.serializers import (
    ServiceRequestSerializer, ServiceResponseSerializer, CreateServiceRequestSerializer, CreateServiceResponseSerializer
)


# Product Views
class ServicesCategoryView(APIView):

    @swagger_auto_schema(tags=["Services"], operation_description='get all product categories',
                         responses={200: ServiceCategorySerailizer(many=True)})
    def get(self, request):
        obj = ServiceCategory.objects.all()

        serializer = ServiceCategorySerailizer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServicesView(APIView):
    Name = openapi.Parameter('Name', openapi.IN_QUERY,
                             description='search by Name', type=openapi.TYPE_STRING)
    CategoryID = openapi.Parameter('CategoryID', openapi.IN_QUERY,
                                   description='search by CategoryID', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(tags=["Services"], operation_description='get products endpoint',
                         manual_parameters=[CategoryID, Name],
                         responses={200: ServiceSerializer(many=True)})
    def get(self, request):
        data = request.query_params

        if 'CategoryID' in data:
            obj = Service.objects.filter(CategoryID_id=data['CategoryID'])
            serializer = ServiceSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if 'Name' in data:
            obj = Service.objects.filter(Name__contains=data['Name'])
            serializer = ServiceSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        obj = Service.objects.all()
        serializer = ServiceSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllServicesView(APIView):

    @swagger_auto_schema(tags=["Services"], operation_description="Endpoint for finding All services",
                         responses={200: InverseCategorySerializer(many=True)})
    def get(self, request):
        products = ServiceCategory.objects.all()

        serializer = InverseCategorySerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPagination(PageNumberPagination):
    page_size = 5


# Pagination with Swagger Sample
# @swagger_auto_schema(
#         operation_description="Endpoint for getting Service Providers response [you may pass all the query params]",
#         manual_parameters=[ProviderID, ProductID, LocationID],
#         responses={200: openapi.Response(
#             description='paginated Services Providers', schema=ServiceProviderSerializer(many=True)
#         )}, paginator=RequestPagination())


class AdvertisementView(APIView):
    @swagger_auto_schema(tags=["Advertisements"], operation_description="Get General list Ads Endpoint",
                         responses={200: AdvertisementSerializer(many=True)})
    def get(self, request):
        ads_obj = Advertisement.objects.all()
        return Response(AdvertisementSerializer(ads_obj, many=True).data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Advertisements"],
                         operation_description="Place an Advert Endpoint <br> Authorized Users only",
                         request_body=CreateAdvertSerializer,
                         responses={201: AdvertisementSerializer(many=False)})
    def post(self, request):
        if request.user:
            data = request.data
            serializer = CreateAdvertSerializer(data=data)
            if serializer.is_valid():
                ad_obj = Advertisement(
                    ADTitle=data["ADTitle"], ProviderID=data['ProviderID'], LocationID_id=data["LocationID"],
                    AdDescription=data["AdDescription"], StartDate=data["StartDate"], ExpiryDate=data["ExpiryDate"]
                )
                ad_obj.save()

                return Response(AdvertisementSerializer(ad_obj, many=False).data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)


region = openapi.Parameter("region", in_=openapi.IN_QUERY, description="search by `region/county`", required=False,
                           type=openapi.TYPE_STRING)


@swagger_auto_schema(
    tags=['Advertisements'], method="GET", operation_description="GET Adverts Request by `Region`",
    manual_parameters=[region], responses={200: AdvertisementSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def getAdvertByRegion(request):
    params = request.query_params
    if "region" in params:
        adverts = Advertisement.objects.filter(LocationID__Name__icontains=params["region"])
        return Response(AdvertisementSerializer(adverts, many=True).data, status.HTTP_200_OK)
    else:
        adverts = Advertisement.objects.all()
        return Response(AdvertisementSerializer(adverts, many=True).data, status.HTTP_200_OK)


class ServiceRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Services Requests"],
                         operation_description="Endpoint for get list of User services requests",
                         responses={200: ServiceRequestSerializer(many=True)})
    def get(self, request):
        if request.user:
            requests = ServiceRequest.objects.filter(UserID=request.user)
            return Response(ServiceRequestSerializer(requests, many=True).data, status.HTTP_200_OK)
        else:
            return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(tags=["Services Requests"],
                         operation_description="Request Service Endpoint <br> Authorized Users only",
                         request_body=CreateServiceRequestSerializer,
                         responses={201: ServiceRequestSerializer(many=False)})
    def post(self, request):
        data = request.data
        serializer = CreateServiceRequestSerializer(data=data)
        if serializer.is_valid():
            if request.user:
                request_obj = ServiceRequest(
                    UserID=request.user, ProviderServiceID_id=data["ProviderServiceID"],
                    CenterLocationID_id=data["CenterLocationID"], Latitude=data["Latitude"],
                    Longitude=data["Longitude"], RequestText=data["RequestText"]
                )
                request_obj.save()

                return Response(ServiceRequestSerializer(request_obj, many=False).data, status.HTTP_201_CREATED)

            else:
                return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=['Services Requests'], method="GET", operation_description="GET Services Request by `Provider`",
    responses={200: ServiceRequestSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def getRequestsByProvider(request):
    if request.user:
        services_request = ServiceRequest.objects.filter(ProviderServiceID__ProviderID__UserID=request.user)

        return Response(ServiceRequestSerializer(services_request, many=True).data, status.HTTP_200_OK)
    else:
        return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    tags=['Services Requests'], method="GET", operation_description="GET Services Request by `Client`",
    responses={200: ServiceRequestSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def getRequestsByClient(request):
    if request.user:
        services_request = ServiceRequest.objects.filter(UserID=request.user)

        return Response(ServiceRequestSerializer(services_request, many=True).data, status.HTTP_200_OK)
    else:
        return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    tags=['Services Requests'], method="GET",
    operation_description="GET Services Request by `Client` but not yet Got Response",
    responses={200: ServiceRequestSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def getRequestNotRespondedByUser(request):
    if request.user:
        services_request = ServiceRequest.objects.filter(
            UserID=request.user, serviceresponse__isnull=True
        )

        return Response(ServiceRequestSerializer(services_request, many=True).data, status.HTTP_200_OK)
    else:
        return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    tags=['Services Requests'], method="GET",
    operation_description="GET Services Request by `Provider` but not yet Responded",
    responses={200: ServiceRequestSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def getRequestNotRespondedByProvider(request):
    if request.user:
        provider = ProviderModel.objects.filter(UserID=request.user).first()
        if provider:
            service_req_obj = ServiceRequest.objects.filter(
                ProviderServiceID__ProviderID__UserID=request.user, serviceresponse__isnull=True
            )
            print("Data")
            return Response(ServiceRequestSerializer(service_req_obj, many=True).data, status.HTTP_200_OK)
        else:
            return Response({"Error": "you are not a service provider"}, status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)


class ServiceResponseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Services Requests"],
                         operation_description="Endpoint for get list of Provider services response",
                         responses={200: ServiceResponseSerializer(many=True)})
    def get(self, request):
        if request.user:
            provider = ProviderModel.objects.filter(UserID=request.user).first()
            if provider:
                response_objs = ServiceResponse.objects.filter(ServiceRequestID__ProviderServiceID__ProviderID=provider)

                return Response(ServiceResponseSerializer(response_objs, many=True).data, status.HTTP_200_OK)
            else:
                return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(tags=["Services Requests"],
                         operation_description="Service Response Endpoint <br> Authorized Users only",
                         request_body=CreateServiceResponseSerializer,
                         responses={201: ServiceResponseSerializer(many=False)})
    def post(self, request):
        data = request.data
        serializer = CreateServiceResponseSerializer(data=data)
        if serializer.is_valid():
            response_obj = ServiceResponse(
                ServiceRequestID_id=data["ServiceRequestID"], ResponseText=data["ResponseText"]
            )
            response_obj.save()

            return Response(ServiceResponseSerializer(response_obj, many=False).data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=['Services Requests'], method="GET", operation_description="GET Services Responses by `Client`",
    responses={200: ServiceResponseSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def getResponseByUser(request):
    if request.user:
        responses = ServiceResponse.objects.filter(ServiceRequestID__UserID=request.user)

        return Response(ServiceResponseSerializer(responses, many=True).data, status.HTTP_200_OK)
    else:
        return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    tags=['Services Requests'], method="GET", operation_description="GET Services Responses by `Provider`",
    responses={200: ServiceResponseSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def getResponsesByProvider(request):
    if request.user:
        provider = ProviderModel.objects.filter(request.user).first()
        if provider:
            responses = ServiceResponse.objects.filter(ServiceRequestID__ProviderServiceID__ProviderID=provider)

            return Response(ServiceResponseSerializer(responses, many=True).data, status.HTTP_200_OK)
        else:
            return Response({"Error": "provider not found"}, status.HTTP_404_NOT_FOUND)
    else:
        return Response({"Error": "User is unauthorized"}, status.HTTP_401_UNAUTHORIZED)
