from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('', include('core.urls')),
    path('',include('orders.urls')),
]
