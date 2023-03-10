from django.contrib import admin
from .models import Cart,CartItem,Coupen,wishlist

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')  

class CoupenAdmin(admin.ModelAdmin):
    list_display=('code','is_active')  
# Register your models here.
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Coupen,CoupenAdmin)
admin.site.register(wishlist)
