from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from main import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('input/', views.InputData.as_view(), name='input'),
    path('input/update/<int:id>', views.handle_input_update, name='input_update'),
    path('generate/queue', views.handle_queue_data, name='record_queue_data'),
    path('currency/', views.Currency.as_view(), name='currencies'),
    path('login/', obtain_auth_token, name='login'),
    path('check/', views.CheckAuth.as_view(), name='test'),
    path('logout/', views.Logout.as_view(), name='logout'),

]
