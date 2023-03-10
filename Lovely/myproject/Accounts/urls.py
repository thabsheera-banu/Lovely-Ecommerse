from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel_order_user/<int:order_number>', views.cancel_order_user, name="cancel_order_user"),
    path('complete_order/<int:order_number>', views.complete_order, name="complete_order"),
    path('contact',views.contact,name='contact'),


]

