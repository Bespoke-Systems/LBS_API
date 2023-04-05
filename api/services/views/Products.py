from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import ProductCategory, Product
from ..serializers.serializer_models import ProductCategorySerailizer, ProductSerializer, InverseCategorySerializer


class productCategoryView(APIView):

    @swagger_auto_schema(operation_description='get all product categories',
                         responses={200: ProductCategorySerailizer(many=True)})
    def get(self, request):
        obj = ProductCategory.objects.all()

        serializer = ProductCategorySerailizer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class productsView(APIView):

    Name = openapi.Parameter('Name', openapi.IN_QUERY,
                             description='search by Name', type=openapi.TYPE_STRING)
    CategoryID = openapi.Parameter('CategoryID', openapi.IN_QUERY,
                                   description='search by CategoryID', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description='get products endpoint', manual_parameters=[CategoryID, Name],
                         responses={200: ProductSerializer(many=True)})
    def get(self, request):
        data = request.query_params

        if 'CategoryID' in data:
            obj = Product.objects.filter(CategoryID_id=data['CategoryID'])
            serializer = ProductSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if 'Name' in data:
            obj = Product.objects.filter(Name__contains=data['Name'])
            serializer = ProductSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        obj = Product.objects.all()
        serializer = ProductSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllProductsView(APIView):

    @swagger_auto_schema(operation_description="Endpoint for finding All services",
                         responses={200: InverseCategorySerializer(many=True)})
    def get(self, request):

        products = ProductCategory.objects.all()

        serializer = InverseCategorySerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)