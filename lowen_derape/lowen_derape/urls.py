from django.contrib import admin
from django.urls import path
from main_app_lowen_button import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_event/', views.add_event, name='add_event'),
]
