from .models import Product
from django.db.models import Max, Min

def filter(request):
    maxx_price = Product.objects.aggregate(Max('price'))['price__max']
    minn_price = Product.objects.aggregate(Min('price'))['price__min']
    return{
        'MAX_price': maxx_price, 
        'MIN_price': minn_price,
    }