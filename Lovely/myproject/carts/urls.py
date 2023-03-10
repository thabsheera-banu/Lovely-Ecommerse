from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('wishlist/',views.wishlistitem,name='wishlist'),
    path('add_to_wishlist/<int:product_id>',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    


]
