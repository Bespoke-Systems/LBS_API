from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import get_user_model
from ..serializers import (
    UserModelSerializer,
    userDetailsValidationSerializer, userPutDetailSerializer, tokenSerializer)

User = get_user_model()


class UserRegister(APIView):

    @swagger_auto_schema(tags=['User'],
                         operation_description='Create new user using Mobile Number, Id/Passport number, First name & '
                                               'Last name',
                         request_body=userDetailsValidationSerializer, responses={201: UserModelSerializer(many=False)})
    def post(self, request):
        data = request.data
        if data:
            validate = userDetailsValidationSerializer(data=data)
            if validate.is_valid():
                valid_number = User.objects.filter(MobileNumber=data['MobileNumber'])
                if valid_number:
                    return Response({'Error': 'User with number already exist'})

                user = User(**data)
                user.save()
                serializer = UserModelSerializer(user, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error': 'please post required data'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['User'],
        operation_description='Update user details with Password , Location & gender.',
        request_body=userPutDetailSerializer, responses={201: tokenSerializer(many=False)}
    )
    def put(self, request):
        data = request.data
        validate = userPutDetailSerializer(data=data)
        if validate.is_valid():
            user = User.objects.get(id=data['UserID'])
            print(user)
            if user:
                user.GenderID_id = data['GenderID']
                user.LocationID_id = data['LocationID']
                user.set_password = data['password']
                user.save()
                token, _ = Token.objects.get_or_create(user=user)

                return Response({'auth_token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return Response({'Error': "User doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)
