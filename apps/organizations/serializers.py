from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.accounts.models import ReceptionistProfile
from .models import Clinic

User = get_user_model()


class ReceptionistProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)

    class Meta:
        model = ReceptionistProfile
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "clinic",
            "profile_image",
            "date_of_birth",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ClinicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = [
            "id",
            "name",
            "address",
            "phone_number",
            "calling_number",
            "email",
            "location_url",
            "city",
            "profile_image",
            "banner_image",
            "is_verified",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "is_verified", "is_active", "created_at"]


class ClinicCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )
    admin_name = serializers.CharField(write_only=True, required=False, default="")

    class Meta:
        model = Clinic
        fields = [
            "name",
            "address",
            "phone_number",
            "calling_number",
            "email",
            "location_url",
            "city",
            "password",
            "admin_name",
        ]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        if Clinic.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A clinic with this phone number already exists.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        admin_name = validated_data.pop("admin_name", "")
        email = validated_data.get("email")
        phone_number = validated_data.get("phone_number")

        with transaction.atomic():
            admin_user = User(
                email=email,
                phone_number=phone_number,
                first_name=admin_name,
                user_role="clinic_admin",
                is_active=True,
            )
            admin_user.set_password(password)
            admin_user.save()

            clinic = Clinic.objects.create(admin=admin_user, **validated_data)

        return clinic


class ReceptionistCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    phone_number = PhoneNumberField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )
    profile_image = serializers.ImageField(required=False, allow_null=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value

    def create(self, validated_data):
        clinic = validated_data.pop("clinic")
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        phone_number = validated_data.pop("phone_number")
        name = validated_data.get("name")

        with transaction.atomic():
            user_obj = User(
                email=email,
                phone_number=phone_number,
                first_name=name,
                user_role="receptionist",
                is_active=True,
            )
            user_obj.set_password(password)
            user_obj.save()

            receptionist = ReceptionistProfile.objects.create(
                user=user_obj,
                clinic=clinic,
                **validated_data
            )
        return receptionist

class AppointmentStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices='Appointment.Status.choices')
