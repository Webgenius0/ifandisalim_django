from django.urls import path
from .views import ConversationList, MessageList
urlpatterns = [
    path('conversations/', ConversationList.as_view(), name='conversations'),
    path('conversations/<str:pk>/messages/', MessageList.as_view(), name='messages'),  # URL for messages page with conversation ID

]
