import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import MenuItem


class BookingApiTests(TestCase):
    def setUp(self):
        self.url = reverse("create-booking")
        self.payload = {
            "first_name": "Mina",
            "reservation_date": "2030-05-14",
            "reservation_slot": 7,
        }

    def post_booking(self, payload):
        return self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_creates_booking_and_rejects_duplicate_slot(self):
        created = self.post_booking(self.payload)

        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["first_name"], "Mina")

        duplicate = self.post_booking(self.payload)
        self.assertEqual(duplicate.status_code, 409)
        self.assertEqual(duplicate.json()["error"], "Slot already booked")

    def test_rejects_invalid_slot(self):
        response = self.post_booking({**self.payload, "reservation_slot": 13})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid date or slot")

    def test_date_endpoint_reports_no_bookings(self):
        response = self.client.get(
            reverse("bookings"), {"date": "2030-05-14"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "No Booking found"})


class RestaurantApiTests(TestCase):
    def test_registration_creates_user_and_token(self):
        response = self.client.post(
            reverse("registration"),
            {"username": "reviewer", "email": "reviewer@example.com", "password": "LemonPass123"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Token.objects.filter(key=response.json()["token"]).exists())

    def test_menu_is_public_and_writes_require_authentication(self):
        MenuItem.objects.create(title="Bruschetta", price="8.50", inventory=12)

        response = self.client.get("/api/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], "Bruschetta")

        response = self.client.post(
            "/api/menu/",
            {"title": "Pasta", "price": "14.00", "inventory": 8},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_token_authenticates_booking_api(self):
        user = get_user_model().objects.create_user(
            username="booker", password="LemonPass123"
        )
        token = Token.objects.create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = client.post(
            "/api/bookings/",
            {
                "first_name": "Mina",
                "reservation_date": "2030-05-14",
                "reservation_slot": 7,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["first_name"], "Mina")