from rest_framework import serializers
from .models import FAQ, StaticPages, ContactUs

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class StaticPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPages
        fields = '__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
