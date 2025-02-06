# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

#create endpounts 

class UserCreateView(APIView):
    authentication_classes = []  # disable authentication
    permission_classes = []  
    def get(self, request): # define endpoint function if i need info
        # return Response(UserSerializer(request.user).data)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AuthStatusView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this endpoint
    def get(self, request):
        return Response({'isAuthenticated': True})
class LoginView(APIView):
    authentication_classes = []  # disable authentication allowing anyone to access the endpoint.
    permission_classes = []  # disable permission
    
    def post(self, request):
        email = request.data.get('email') #DRF automatically parses the incoming JSON payload.
        print(f"Trying to authenticate: {email}")
        password = request.data.get('password') 
        user = authenticate(request, email=email, password=password) #returns a user object
        print (f"Authenticated user: {user}")
         
        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({
                'success': True,
                'access': str(refresh.access_token)
                }) #Generates a new refresh token for the user.
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                path='api/token/refresh/'
            )
            return response
        print("Authentication failed")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response({'message': 'logged out'})
        response.delete_cookie('refresh_token') #refresh token
        return response
         
    # def post(self, request):
    # email = request.data.get('email')
    # password = request.data.get('password')

    # print(f"Received login request for email: {email}")

    # user = authenticate(request, username=email, password=password)

    # if not user:
    #     print("Authentication failed. Checking user manually...")
    #     user = User.objects.filter(email=email).first()
    #     if user:
    #         print(f"User found: {user}")
    #         if user.check_password(password):
    #             print("Password is correct.")
    #         else:
    #             print("Incorrect password.")
    #     else:
    #         print("User does not exist.")

    #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    # print(f"Authenticated user: {user}")

    # refresh = RefreshToken.for_user(user)
    # response = Response({'access': str(refresh.access_token)})
    # response.set_cookie(
    #     key='refresh_token',
    #     value=str(refresh),
    #     httponly=True,
    #     secure=True,
    #     samesite='Lax',
    #     path='api/token/refresh/'
    # )
    # return response
   
    
    
    
    
    
    
    
    
    
    
    
    

# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail(self, request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data) #for specific user

#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save() #update users info
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

