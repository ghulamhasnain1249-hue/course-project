from django.contrib import admin

from .models import Booking, MenuItem


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("first_name", "reservation_date", "reservation_slot")
    list_filter = ("reservation_date",)
    ordering = ("reservation_date", "reservation_slot")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "inventory")
    search_fields = ("title",)