from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-customer/', views.create_customer, name='create-customer'),
    path('json/', views.json, name='json'),
    path('template-view/', views.ExampleTemplateView.as_view(), name='json'),
]