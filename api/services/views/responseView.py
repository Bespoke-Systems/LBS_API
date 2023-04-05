from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from services.models import (
    RequestResponse
)
from services.serializers.serializer_models import (
    RequestResponseSerializer
)
from services.serializers.serializer_forms import ServiceResponseCreationSerializer

class RequestedResponseView(APIView):

    ResponseID = openapi.Parameter('ResponseID', openapi.IN_QUERY, description="Get by ResponseID param(optional)", type=openapi.TYPE_INTEGER)
    RequestID = openapi.Parameter('RequestID', openapi.IN_QUERY, description="Get by RequestID param(optional)", type=openapi.TYPE_INTEGER)
    ProviderID = openapi.Parameter('ProviderID', openapi.IN_QUERY, description="Get by ProviderID param(optional)", type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(operation_description="Endpoint for filtering Service responses by either params or All*", manual_parameters=[ResponseID, RequestID, ProviderID], responses={200: RequestResponseSerializer(many=True)})
    def get(self, request):

        data = request.query_params
        if "ResponseID" in data:
            response = RequestResponse.objects.filter(id=data["ResponseID"])
            serializer = RequestResponseSerializer(response, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        if "RequestID" in data:
            response = RequestResponse.objects.filter(RequestID_id=data["RequestID"])
            serializer = RequestResponseSerializer(response, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        if "ProviderID" in data:
            response = RequestResponse.objects.filter(ProviderID_id=data["ProviderID"])
            serializer = RequestResponseSerializer(response, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        
        response = RequestResponse.objects.all()
        serializer = RequestResponseSerializer(response, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=ServiceResponseCreationSerializer,responses={201: RequestResponseSerializer(many=False)}
    )
    def post(self, request):
        data = request.data
        serializer = ServiceResponseCreationSerializer(data=data)
        if serializer.is_valid():
            response = RequestResponse(RequestID_id=data["RequestID"], ProviderID_id=data["ProviderID"])
            if data["ResponseText"] is not None:
                response.ResponseText = data["ResponseText"]
            try:
                response.save()
                serializer = RequestResponseSerializer(response, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"Error": ["Db RequestID or ProviderID IntegrityError constraint failed"]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
