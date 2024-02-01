from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
chat_router = DefaultRouter()
message_router = DefaultRouter()
chat_router.register('', ChatViewSet, basename='chat')
message_router.register('', MessageViewSet, basename='message')

urlpatterns = [
    path('api/chat/', include(chat_router.urls)),
    path('api/chat/<int:chat_id>/message/', include(message_router.urls)),
    # path('api/chats/<int:chat_id>/', ChatDetailView.as_view(), name='chat-detail'),
    # path('api/chats/<int:chat_id>/messages/<int:message_id>/', MessageDetailView.as_view(), name='message-detail'),
]

