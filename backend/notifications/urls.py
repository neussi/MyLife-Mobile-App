from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:pk>/read/', views.mark_read, name='mark_notification_read'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_notifications_read'),
    path('settings/', views.notification_settings, name='notification_settings'),
    path('api/unread-count/', views.unread_count_api, name='unread_count_api'),
]
