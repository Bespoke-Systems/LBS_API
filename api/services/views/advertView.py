from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from services.models import Advertisement
from services.serializers.serializer_models import AdvertisementSerializer

class AdvertView(APIView):

    UserID = openapi.Parameter('UserID', openapi.IN_QUERY, description="Get by UserID id param(optional)", type=openapi.TYPE_INTEGER)
    ProductID = openapi.Parameter('ProductID', openapi.IN_QUERY, description="Get by ProductID id param(optional)", type=openapi.TYPE_INTEGER)
    LocationID = openapi.Parameter('LocationID', openapi.IN_QUERY, description="Get by LocationID id param(optional)", type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(operation_description="Endpoint for requesting and serching ads", manual_parameters=[UserID, ProductID, LocationID], responses={200: AdvertisementSerializer(many=True)})
    def get(self, request):
        data = request.query_params
        if data["UserID"] and data["ProductID"] and data["LocationID"] is not None:
            adverts = Advertisement.objects.filter(UserID_id=data["UserID"], ProductID_id=data["ProductID"], LocationID_id=data["LocationID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if data["UserID"] and data["ProductID"] is not None:
            adverts = Advertisement.objects.filter(UserID_id=data["UserID"], ProductID_id=data["ProductID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if data["LocationID"] and data["ProductID"] is not None:
            adverts = Advertisement.objects.filter(LocationID_id=data["LocationID"], ProductID_id=data["ProductID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if data["UserID"] is not None:
            adverts = Advertisement.objects.filter(UserID_id=data["UserID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if data["ProductID"] is not None:
            adverts = Advertisement.objects.filter(ProductID_id=data["ProductID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if data["LocationID"] is not None:
            adverts = Advertisement.objects.filter(LocationID_id=data["LocationID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        adverts = Advertisement.objects.all()
        serializer = AdvertisementSerializer(adverts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(
        request_body=openapi.Schema(description="Create an AD as a User", type=openapi.TYPE_OBJECT,required=['UserID'],
            properties={
                'UserID': openapi.Schema(description="UserID id", type=openapi.TYPE_INTEGER),
                'ProductID': openapi.Schema(description="ProductID id", type=openapi.TYPE_INTEGER),
                'LocationID': openapi.Schema(description="LocationID id(optional)", type=openapi.TYPE_INTEGER),
                'ADText': openapi.Schema(description="ADText text(optional)", type=openapi.TYPE_STRING),
                'GenderID': openapi.Schema(description="To target gender(optional)", type=openapi.TYPE_INTEGER),
                'ExpiryDate': openapi.Schema(description="Expires on certain datetime(optional)", type=openapi.TYPE_STRING),
                'NoOfMessages': openapi.Schema(description="Send this number of ADs(optional)", type=openapi.TYPE_INTEGER),
            }
        ),responses={201: AdvertisementSerializer(many=False)}
    )  
    def post(self, request):
        data = request.data
        if data["UserID"] is not None:
            advert = Advertisement(UserID_id=data["UserID"])
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if data["ProductID"] is not None:
            advert.ProductID_id = data["ProductID"]
        if data["LocationID"] is not None:
            advert.LocationID_id = data["LocationID"]
        if data["ADText"] is not None:
            advert.ADText = data["ADText"]
        if data["GenderID"] is not None:
            advert.GenderID_id = data["GenderID"]
        if data["ExpiryDate"] is not None:
            try:
                advert.ExpiryDate = data["ExpiryDate"]
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if data["NoOfMessages"] is not None:
            advert.NoOfMessages = data["NoOfMessages"]
        advert.save()
        serializer = AdvertisementSerializer(advert, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)