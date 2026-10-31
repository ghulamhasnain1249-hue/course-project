import json
from datetime import datetime

from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .models import Booking

BOOKING_SLOTS = {
    1: "10:00",
    2: "11:00",
    3: "12:00",
    4: "13:00",
    5: "14:00",
    6: "15:00",
    7: "16:00",
    8: "17:00",
    9: "18:00",
    10: "19:00",
    11: "20:00",
    12: "21:00",
}


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def menu(request):
    return render(request, "menu.html")


def book(request):
    return render(request, "book.html")


def reservations(request):
    return render(request, "reservations.html")


def _booking_data(booking):
    return {
        "id": booking.id,
        "first_name": booking.first_name,
        "reservation_date": booking.reservation_date.isoformat(),
        "reservation_slot": booking.reservation_slot,
        "slot_time": BOOKING_SLOTS.get(booking.reservation_slot, ""),
    }


@require_GET
def bookings(request):
    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({"error": "Date parameter required"}, status=400)

    try:
        reservation_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format"}, status=400)

    items = Booking.objects.filter(reservation_date=reservation_date).order_by(
        "reservation_slot"
    )
    data = [_booking_data(booking) for booking in items]
    if not data:
        return JsonResponse({"message": "No Booking found"}, safe=False)
    return JsonResponse(data, safe=False)


@require_GET
def all_bookings(request):
    items = Booking.objects.all().order_by("reservation_date", "reservation_slot")
    return JsonResponse([_booking_data(booking) for booking in items], safe=False)


@require_POST
def create_booking(request):
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not isinstance(body, dict):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    first_name = body.get("first_name")
    date_str = body.get("reservation_date")
    slot = body.get("reservation_slot")

    if not isinstance(first_name, str) or not first_name.strip() or date_str is None or slot is None:
        return JsonResponse({"error": "Missing fields"}, status=400)

    try:
        reservation_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        slot = int(slot)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid date or slot"}, status=400)

    if slot not in BOOKING_SLOTS:
        return JsonResponse({"error": "Invalid date or slot"}, status=400)

    try:
        with transaction.atomic():
            booking = Booking.objects.create(
                first_name=first_name.strip(),
                reservation_date=reservation_date,
                reservation_slot=slot,
            )
    except IntegrityError:
        return JsonResponse({"error": "Slot already booked"}, status=409)

    return JsonResponse(_booking_data(booking), status=201)