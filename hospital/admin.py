from django.contrib import admin
from .models import Patient, MedicalRecord

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('health_id', 'name', 'phone', 'age', 'blood_group')
    search_fields = ('health_id', 'name', 'phone')
    list_filter = ('blood_group', 'language')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'date', 'diagnosis', 'doctor')
    search_fields = ('patient__name', 'patient__health_id', 'diagnosis')
    list_filter = ('date', 'doctor')
    readonly_fields = ('patient',)
