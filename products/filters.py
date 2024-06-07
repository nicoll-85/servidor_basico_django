import django_filters
from .models import (Product,Sale)

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['brand']
        
class SaleFilter(django_filters.FilterSet):
    class Meta:
        model = Sale
        fields = ['date']