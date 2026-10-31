from django.contrib.auth import get_user_model
from rest_framework import generics, serializers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import Booking, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    def validate_reservation_slot(self, value):
        if not 1 <= value <= 12:
            raise serializers.ValidationError("Choose a reservation slot from 1 to 12.")
        return value


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password")
        read_only_fields = ("id",)

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all().order_by("id")
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("reservation_date", "reservation_slot")
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"id": user.pk, "username": user.username, "token": token.key},
            status=status.HTTP_201_CREATED,
        )