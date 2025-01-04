from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class ConversationList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        conversation = Conversation.objects.filter(user=request.user)
        serializer = ConversationSerializer(conversation, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    








class MessageList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        message = Message.objects.filter(user=request.user)
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        conversation = Conversation.objects.get(pk=pk)
        print("dfgdkf",conversation)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(conversation=conversation)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)