
from django.contrib import admin
from django.urls import path, include
from hospital.views import About

urlpatterns = [
    path('admin/', admin.site.urls),
    # root landing page
    path('', About, name='home'),
    path('About/', About, name='About'),
    # include hospital app endpoints (patient-login, add-record, etc.)
    path('', include('hospital.urls')),
]
