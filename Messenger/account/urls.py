from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
user_router = DefaultRouter()
user_router.register('', UserViewSet, basename='user')

contact_router = DefaultRouter()
contact_router.register('', ContactViewSet, basename='contact')

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/users/', include(user_router.urls)),
    path('api/users/<int:user_id>/contacts/', include(contact_router.urls), name='contact-list'),

    path('api/checkusername/', CheckUsernameAPI.as_view()),
    path('api/checkphone/', CheckPhoneAPI.as_view()),

    path('api/getcontact/<int:pk>/', ChatContact.as_view(), name='register'),

]
