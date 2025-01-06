from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.transaction_webhook, name='webhook'),
    
]