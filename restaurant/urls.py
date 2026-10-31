from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .api import BookingViewSet, MenuItemViewSet, RegistrationView

router = DefaultRouter()
router.register("menu", MenuItemViewSet)
router.register("bookings", BookingViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/registration/", RegistrationView.as_view(), name="registration"),
    path("api-token-auth/", obtain_auth_token, name="api-token-auth"),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("menu/", views.menu, name="menu"),
    path("book/", views.book, name="book"),
    path("reservations/", views.reservations, name="reservations"),
    path("bookings", views.bookings, name="bookings"),
    path("bookings/all", views.all_bookings, name="all-bookings"),
    path("bookings/create", views.create_booking, name="create-booking"),
]