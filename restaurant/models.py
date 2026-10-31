from django.db import models


class Booking(models.Model):
    first_name = models.CharField(max_length=255)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("reservation_date", "reservation_slot"),
                name="unique_booking_date_slot",
            )
        ]

    def __str__(self):
        return f"{self.first_name} - {self.reservation_date} - {self.reservation_slot}"


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title