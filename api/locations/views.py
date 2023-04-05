from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import TownsModel, CountyModel
from .serializers import TownsModelSerializer, CountyModelSerializers, LocationSerializer


class CountyView(APIView):

    @swagger_auto_schema(operation_description="Endpoint for getting counties",
                         responses={200: CountyModelSerializers(many=True)})
    def get(self, request):
        counties = CountyModel.objects.all()
        serializer = CountyModelSerializers(counties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TownsView(APIView):
    CountyID = openapi.Parameter('CountyID', openapi.IN_QUERY, description="Search by CountyID(optional)",
                                 type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Endpoint for searching town locations", manual_parameters=[CountyID],
                         responses={200: TownsModelSerializer(many=True)})
    def get(self, request):
        data = request.query_params
        if "CountyID" in data:
            towns = TownsModel.objects.filter(County_id=data["CountyID"])
            serializer = TownsModelSerializer(towns, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        towns = TownsModel.objects.all()
        serializer = TownsModelSerializer(towns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocationApi(APIView):

    @swagger_auto_schema(operation_description="Endpoint for finding locations",
                         responses={200: LocationSerializer(many=True)})
    def get(self, request):
        locations = CountyModel.objects.all()

        serializer = LocationSerializer(locations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
