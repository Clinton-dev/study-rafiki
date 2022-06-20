from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('register/', views.register, name='register'),


    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),

    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-comment/<str:pk>/', views.deleteComment, name='delete-comment'),
    path('update-comment/<str:pk>/', views.updateComment, name='update-comment'),

    path('profile/<str:pk>', views.userProfile, name='user-profile')
]