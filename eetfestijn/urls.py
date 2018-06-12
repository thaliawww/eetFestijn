from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^(?i)admin/', include(admin.site.urls)),
    url(r'^(?i)wiebetaaltwat/', include('wiebetaaltwat.urls')),
    url(r'^(?i)', include('orders.urls')),
]
