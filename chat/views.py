from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import openai
from django.conf import settings

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
    
class ChatGPTService:
    @staticmethod
    def ask_gpt(prompt: str) -> str:
        openai.api_key = settings.OPENAI_API_KEY
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # You can also use "gpt-4" if you have access
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7,
            )
            return response['choices'][0]['message']['content']
        except openai.error.OpenAIError as e:
            return str(e)










class MessageList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        message = Message.objects.filter(user=request.user)
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        conversation = Conversation.objects.get(pk=pk)

        prompt = request.data.get('question', '')
        response = ChatGPTService.ask_gpt(prompt)
        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(conversation=conversation, answer = response)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)