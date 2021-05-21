from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from main import views
from main.views import CustomAuthToken

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('input/', views.InputData.as_view(), name='input'),
    path('input/update/<int:id>', views.handle_input_update, name='input_update'),
    path('generate/queue', views.handle_queue_data, name='record_queue_data'),
    path('currency/', views.Currency.as_view(), name='currencies'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('check/', views.CheckAuth.as_view(), name='test'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('Recorded/Data/<int:Input>', views.RecordedDataList.as_view(), name='recorded_data'),
    path('retrieve/input/<int:pk>', views.InputRetrieve.as_view(), name='retrieve_input'),
    path('account/<int:pk>', views.AccountRetrieveUpdate.as_view(), name='account_retrieve_update'),
    path('exchange/', views.ExchangeCompany.as_view(), name='exchange'),
    path('log/<int:input_id>', views.LogsData.as_view(), name='logs')

]
