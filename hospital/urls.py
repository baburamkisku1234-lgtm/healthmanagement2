# hospital/urls.py

from django.urls import path                # ← import path
from .views import add_record, patient_login, patient_records, register, search_patient            # ← import the view you’re routing to

urlpatterns = [
    path("register/", register, name="register"),
    path("patient-login/", patient_login, name="patient_login"),
    path("add-record/",add_record),
    path("search-patient/", search_patient, name="search_patient"),
    path("records/<str:health_id>/", patient_records),
]