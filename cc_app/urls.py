from django.urls import path

from cc_app import views

app_name = 'cc_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('information/', views.information, name='information'),
    path('portal/', views.portal, name='portal'),
    path('logout/', views.logout, name='logout'),
    path('log/', views.log, name='log'),

]
