from django.urls import path
from . import views

urlpatterns =[
    path('pages/', views.StaticPagesList.as_view()),
    path('contact/', views.ContactUsCreate.as_view()),
    path('faq/', views.FAQView.as_view()),

]