from django.urls import path

from meals import views

app_name = 'meals'

urlpatterns = [
    path('', views.meal, name='index'),
]
