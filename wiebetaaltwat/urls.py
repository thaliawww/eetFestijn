from django.urls import path

from . import views

urlpatterns = [
    path('update-list/', views.update_lists, name='update_list'),
]
