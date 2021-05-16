from django.urls import path

from main import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('input/', views.Input.as_view(), name='input')

]
