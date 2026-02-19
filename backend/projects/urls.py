from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('<int:project_pk>/milestones/create/', views.milestone_create, name='milestone_create'),
    path('milestones/<int:pk>/toggle/', views.milestone_toggle, name='milestone_toggle'),
    path('milestones/<int:pk>/delete/', views.milestone_delete, name='milestone_delete'),
]
