from django.urls import path

from main import views

urlpatterns = [
    path('register/', views.Register.as_view())

]
