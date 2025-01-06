from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status 


from .models import ContactUs, StaticPages, FAQ
from .serializers import StaticPagesSerializer, ContactUsSerializer, FAQSerializer

class StaticPagesList(APIView):
    
    def get(self, request, format=None):
        queryset = StaticPages.objects.all()
        serializer = StaticPagesSerializer(queryset, many=True)
        return Response(
            {
            "status":"success",
            "messae": "Static pages retrived successfully",
            "data": serializer.data
            }
        )


class ContactUsCreate(APIView):
    def post(self, request, format=None):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success", "message":"Message sent to admin successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FAQView(APIView):
    def get(self, request, format=None):
        queryset = FAQ.objects.all()
        serializer = FAQSerializer(queryset, many=True)
        return Response(
            {
            "status":"success",
            "message": "FAQs retrived successfully",
            "data": serializer.data
            }
        )