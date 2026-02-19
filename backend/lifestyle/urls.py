from django.urls import path
from . import views

urlpatterns = [
    path('', views.lifestyle_dashboard, name='lifestyle_dashboard'),
    path('habits/create/', views.habit_create, name='habit_create'),
    path('habits/<int:pk>/edit/', views.habit_edit, name='habit_edit'),
    path('habits/<int:pk>/delete/', views.habit_delete, name='habit_delete'),
    path('habits/<int:pk>/toggle/', views.habit_toggle, name='habit_toggle'),
    path('mood/log/', views.mood_log, name='mood_log'),
    path('mood/<int:pk>/edit/', views.mood_edit, name='mood_edit'),
    path('mood/<int:pk>/delete/', views.mood_delete, name='mood_delete'),
]
