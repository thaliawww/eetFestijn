from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wiebetaaltwat/', include('wiebetaaltwat.urls')),
    path('fest/', include('orders.urls')),
    path('split/', include('meals.urls')),
    path('', TemplateView.as_view(template_name='eetfestijn/index.html'))
]
