from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('my/', views.user_orders, name='user_orders'),
    path('create/<int:book_id>/', views.create_order, name='create_order'),
    path('close/<int:order_id>/', views.close_order, name='close_order'),
]