from django.urls import path
from . import views

urlpatterns = [
    path('insight/', views.get_advisor_insight, name='advisor_insight'),
]
