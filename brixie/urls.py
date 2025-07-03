from django.urls import path
from .views import ChatAPIView, chat_ui

urlpatterns = [
    path('chat/', ChatAPIView.as_view(), name='chat-api'),
    path('', chat_ui, name='chat-ui'),

]
