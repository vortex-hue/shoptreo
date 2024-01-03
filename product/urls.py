from django.urls import path, include

from product import views

urlpatterns = [
    path('products/', views.Products.as_view()),
    path('products/search/', views.search),
    path('product/<int:pk>/', views.Product_.as_view(), name='product'),

]