from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializers import CreateAuthToken, LoginResponseSerializer


User = get_user_model()


def postUserLogin(data):
    user = User.objects.filter(MobileNumber=data["MobileNumber"]).first()

    if user:
        if user.check_password(data["password"]):
            return user
        else:
            return {"error": ["Invalid user creditentials"]}
    else:
        return {"error": ["User not found"]}


class LoginJwtToken(APIView):

    @swagger_auto_schema(tags=['User'], operation_description="Get JWT token Header",
                         request_body=CreateAuthToken,
                         responses={200: LoginResponseSerializer(many=False)}
                         )
    def post(self, request):
        post_data = request.data
        serializer = CreateAuthToken(data=post_data)
        if serializer.is_valid():
            user = postUserLogin(post_data)
            try:
                token, _ = Token.objects.get_or_create(user_id=user.id)
                results = LoginResponseSerializer({
                    "MobileNumber": user.MobileNumber, "FirstName": user.FirstName,
                    "Auth_token": token.key
                }, many=False)
                return Response(results.data, status.HTTP_200_OK)

            except:
                return Response(user, status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LogOutJwtToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    response = openapi.Schema('User', openapi.IN_BODY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(tags=['User'], operation_description="Delete JWT token Header",
                         responses={200: response}
                         )
    def post(self, request):
        print(request.user)
        request.user.auth_token.delete()
        return Response({"User": "succesfully log out"}, status.HTTP_200_OK)
