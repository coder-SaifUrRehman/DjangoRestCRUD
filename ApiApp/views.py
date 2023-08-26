from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import UserFilter
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin


from rest_framework.authentication import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


# Create your views here.



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']  #filter the data with name field as below  given..
    filterset_class = UserFilter
    search_fields = ['name', 'email']  #search the data with name field and email ..
    ordering_fields = ['name'] #order the data with name field
    # pagination_class= PageNumberPagination # paginate the data according to the page size defined in settings.py
    pagination_class= LimitOffsetPagination # provide the customized pagination with limit that how much items that  you want to show. And offset describe the num of items to skip.
    throttle_classes = [AnonRateThrottle,UserRateThrottle]







    # filtering queryset by providing user_name in url along with user_name?
    # def get_queryset(self):
    #     queryset = User.objects.all()
    #     user_name = self.request.query_params.get('user_name')# same as below
    #     user_name = self.request.GET.get('user_name')
    #     if user_name is not None:
    #         return queryset.filter(name=user_name)
    #     return queryset

      
 
# class AddUserView(ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class DeleteUserView(RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     # lookup_field = 'id'   #to speacify field other than pk field...


# class AddUserView(ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class DeleteUserView(RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     # lookup_field = 'id'   #to speacify field other than pk field...




#<--------------------------------Class Based Views------------------------------------->





# class UserAPIView(APIView):
#     def get(self, request, pk=None, format=None):
#         if pk is not None:
#             user = User.objects.get(pk=pk)
#             serializer = serializers.UserSerializer(user)
#             return Response(serializer.data)

#         user = User.objects.all()
#         serializer = serializers.UserSerializer(user, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = serializers.UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'user Created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk, format=None):
        
#         user = User.objects.get(pk = pk)
#         serializer = serializers.UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Complete user Updated'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk, format=None):
        
#         user = User.objects.get(pk=pk)
#         serializer = serializers.UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Partial user Updated'})
#         return Response(serializer.errors)

#     def delete(self, request, pk, format=None):
#         user = User.objects.get(pk=pk)
#         user.delete()
#         return Response({'msg': 'user Deleted'})


# class based Authentication views

class ClassBasedToken(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({"access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Logout view 
from rest_framework_simplejwt.exceptions import TokenError

# class LogoutView(APIView):
#     def post(self, request):
#         token = request.data.get('token')
#         if token:
#             try:
#                 token_obj = RefreshToken(token)
#                 token_obj.blacklist()
#                 return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
#             except TokenError as e:
#                 return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"message": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView, BlacklistMixin):
    def post(self, request):
        
    
        token = request.data.get('refresh')
        if token:
            try:

                token = RefreshToken(token)
                token.blacklist()
                return Response({"message": "Logout successful"})
            except TokenError as e:
                return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)