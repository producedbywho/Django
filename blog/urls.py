from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='index'),
    path('create/', views.post_create, name='post_create'),
    path('<int:id>/', views.post_detail, name='post_detail'),
]
