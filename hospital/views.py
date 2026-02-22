from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

from .models import Patient, MedicalRecord
from django.core.exceptions import ObjectDoesNotExist
import uuid

@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"status": "fail", "error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "fail", "error": "invalid JSON"}, status=400)

    # create a unique health id
    hid = "KW" + uuid.uuid4().hex[:8].upper()
    p = Patient.objects.create(
        health_id=hid,
        phone=data.get("phone", ""),
        name=data.get("name", ""),
        age=data.get("age"),
        blood_group=data.get("bloodGroup", ""),
        language=data.get("language", ""),
    )
    return JsonResponse({"patient_id": p.health_id})


@csrf_exempt
def patient_login(request):
    if request.method != "POST":
        return JsonResponse({"status": "fail", "error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "fail", "error": "invalid JSON"}, status=400)

    try:
        p = Patient.objects.get(health_id=data["health_id"])
    except (KeyError, ObjectDoesNotExist):
        return JsonResponse({"status": "fail"}, status=400)

    # compare phone numbers explicitly
    if p.phone == data.get("phone"):
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "fail"}, status=401)


# simple informational page
# the template 'about.html' is located under hospital/templates/about.html
# this view is referenced by the project URLconf (healthmanagement/urls.py)
def About(request):
    # could use HttpResponse or render a template
    return render(request, "about.html")


@csrf_exempt
def add_record(request):
    if request.method != "POST":
        return JsonResponse({"status": "fail", "error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "fail", "error": "invalid JSON"}, status=400)

    try:
        p = Patient.objects.get(health_id=data["health_id"])
    except ObjectDoesNotExist:
        return JsonResponse({"status": "fail", "error": "patient not found"}, status=404)

    MedicalRecord.objects.create(
        patient=p,
        date=data.get("date"),
        description=data.get("description", ""),
        diagnosis=data.get("diagnosis", ""),
        prescription=data.get("prescription", ""),
        doctor=data.get("doctor", "")
    )

    return JsonResponse({"status": "saved"})


@csrf_exempt
def patient_records(request, health_id):
    if request.method != "GET":
        return JsonResponse({"status": "fail", "error": "GET required"}, status=405)

    try:
        p = Patient.objects.get(health_id=health_id)
    except ObjectDoesNotExist:
        return JsonResponse({"status": "fail", "error": "patient not found"}, status=404)

    records = MedicalRecord.objects.filter(patient=p)

    data = []
    for r in records:
        data.append({
            "date": str(r.date),
            "description": r.description,
            "diagnosis": r.diagnosis,
            "prescription": r.prescription,
            "doctor": r.doctor,
        })

    return JsonResponse({"records": data})


@csrf_exempt
def search_patient(request):
    """Search for a patient by health_id and return basic info."""
    if request.method != "GET":
        return JsonResponse({"status": "fail", "error": "GET required"}, status=405)

    health_id = request.GET.get("health_id", "").strip()
    if not health_id:
        return JsonResponse({"status": "fail", "error": "health_id required"}, status=400)

    try:
        p = Patient.objects.get(health_id=health_id)
        return JsonResponse({
            "status": "ok",
            "patient": {
                "health_id": p.health_id,
                "name": p.name,
                "age": p.age,
                "phone": p.phone,
                "blood_group": p.blood_group,
                "language": p.language,
            }
        })
    except ObjectDoesNotExist:
        return JsonResponse({"status": "fail", "error": "patient not found"}, status=404)
