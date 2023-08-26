from django.urls import path, include
# from .views import AddUserView, DeleteUserView, UserViewSet
from .views import  ClassBasedToken, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 

# from ApiApp import views



urlpatterns = [

    # path('add/', AddUserView.as_view(), name='add'),
    # path('add/<int:pk>', DeleteUserView.as_view(), name='del'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('ctoken/', ClassBasedToken.as_view(), name='obtain_token'),
    path('logout/', LogoutView.as_view(), name='logout'),

] 
