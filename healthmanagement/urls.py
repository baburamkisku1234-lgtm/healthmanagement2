
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # delegate root and app routes to hospital.urls
    path('', include('hospital.urls')),
]
