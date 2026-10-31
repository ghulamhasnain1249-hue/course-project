from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=255)),
                ("reservation_date", models.DateField()),
                ("reservation_slot", models.SmallIntegerField(default=10)),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("reservation_date", "reservation_slot"),
                        name="unique_booking_date_slot",
                    )
                ],
            },
        ),
    ]