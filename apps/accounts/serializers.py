from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import City, DoctorProfile, PatientProfile, ReceptionistProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "user_role",
            "is_active",
            "is_phone_verified",
        ]
        read_only_fields = ["id", "username", "is_phone_verified"]


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, min_length=6, max_length=6)
    user_role = serializers.ChoiceField(
        choices=[
            ("doctor", "Doctor"),
            ("patient", "Patient"),
            ("receptionist", "Receptionist"),
            ("clinic_admin", "Clinic Admin"),
        ],
        required=False,
        default="patient",
    )


class UsernameLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


