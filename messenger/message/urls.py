from django.urls import path
from message import views


app_name = 'chat'

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('', views.chat, name='chat'),
    path('create-message/', views.create_message, name='create-message'),
    path('stream-chat-messages/', views.stream_chat_messages, name='stream-chat-messages'),
]
