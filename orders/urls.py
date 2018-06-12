from django.urls import path

from orders import views

urlpatterns = [
    path('', views.index, name='index'),
    path('summary/', views.summary, name='summary'),
    path('summary.pdf', views.summary_PDF, name='summary_PDF'),
    path('overview/', views.overview, name='overview'),
    path('receipts/', views.receipts, name='receipts'),
    path('print/', views.print_script, name='print_script'),
]
