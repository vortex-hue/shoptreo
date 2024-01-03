
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer

@api_view(['POST'])
## for productiom
## @authentication_classes([authentication.TokenAuthentication])

@authentication_classes([authentication.BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        # Calculate the total paid amount
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        # Save the order instance with the user and paid amount
        serializer.save(user=request.user, paid_amount=paid_amount)

        # Return the order data
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # Return errors if the data is not valid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OrdersList(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    ## in production
    ##  authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    
    
## this includes the docs

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {
            'Endpoint': '/api/v1/auth/users/',
            'method': 'GET, POST, PUT, HEAD, OPTIONS',
            'body': "Since the docs utilized is the django normal docs, and not swagger docs, and BasicAuthenticated is utilized, kindly use the username 'admin' and password 'password' to login, and be authenticated to proceed with calling authenticated endpoints ",
            'description': 'This handles everything that has to do with authentication'
        },
        {
            'Endpoint': '/api/v1/products/',
            'method': 'GET',
            'body': None,
            'description': 'Grabs and lists all the products in the database'
        },
          {
            'Endpoint': '/api/v1/products/',
            'method': 'POST',
            'body': {
                "name": "product name",
                "description": "product description",
                "price": 200.00,
                "get_image": "",
                "get_thumbnail": "",
                "stock_quantity": 212,
                "category": 1  
            },
            'description': 'Creates a new product in a category, but category is created in the backend'
        },
        {
            'Endpoint': '/api/v1/product/<int:pk>/',
            'method': 'PUT',
            'body': {
                "name": "product name updated",
                "description": "product description updated",
                "price": 200.00,
                "get_image": "",
                "get_thumbnail": "",
                "stock_quantity": 212,
                "category": 1  
            },
            'description': 'updates the infos in a product'
        },
        {
            ##'Delete Function',
            "Endpoint": "/api/v1/product/<int:pk>/" ,
            "Body": "curl -X DELETE http://liveurl.com/api/v1/product/1/",
            "Description": "I used curl to make an api request instead, because delete doesn't necessarily requires a body"
        },
          {
            'Endpoint': '/api/v1/checkout/',
            'method': 'POST, OPTIONS',
            'Authenticated' : True,
            'body': {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.com",
                "zipcode": "12345",
                "place": "City, State",
                "phone": "123-456-7890",
                "address": "123 Example Street, City, State, Zip Code",
                "items": [
                    {
                        "product": 1,  # Assuming 6 is the product ID
                        "quantity": 12, # Quantity being ordered
                        "price": 2200.00 # Price per unit of the product
                    }
                ]
            },
            'description': 'Creates a checkout, and instantiates an order instance, on a production levels, payments would be collected'
        },
          {
            'Endpoint': '/api/v1/orders/',
            'method': 'GET',
            'Authenticated' : True,
            'body': None,
            'description': 'Gets all orders associated with the authenticated user'
        },
        
    ]
    return Response(routes)


