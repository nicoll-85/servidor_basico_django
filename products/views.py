from django.shortcuts import render
from .models import (Product,Sale)
from .serializers import (Productserializer,Saleserializer)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import (ProductFilter,SaleFilter)
    
# Vistas genericas Producto
class ProductListCreate(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=Productserializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=Productserializer

class ProductListByBrand(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class = Productserializer

    def get_queryset(self):
        brand = self.kwargs['brand']
        return Product.objects.filter(brand=brand)
    
class ProductListByType(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class = Productserializer

    def get_queryset(self):
        product_type = self.kwargs['product_type']
        return Product.objects.filter(product_type=product_type)
    
# Vistas genericas Ventas
class SaleListCreate(generics.ListCreateAPIView):
    queryset=Sale.objects.all()
    serializer_class=Saleserializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SaleFilter

class SaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Sale.objects.all()
    serializer_class=Saleserializer

class SaleListByDate(generics.ListAPIView):
    queryset=Sale.objects.all()
    serializer_class = Saleserializer

    def get_queryset(self):
        date = self.kwargs['date']
        return Sale.objects.filter(date=date)

class SaleListByProduct(generics.RetrieveUpdateDestroyAPIView):
    queryset=Sale.objects.all()
    serializer_class = Saleserializer

# Vista propia que enlaza los modelos
class ProductSalesAPIView(APIView):
    def get(self, request, product_id):
        try:
            product_id = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        sales = Sale.objects.filter(product_id=product_id)
        sales_serializer = Saleserializer(sales, many=True)
        product_serializer = Productserializer(product_id)
        
        response_data = {
            'product': product_serializer.data,
            'sales': sales_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
