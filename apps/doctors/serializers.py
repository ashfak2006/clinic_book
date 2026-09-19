from rest_framework import serializers
from apps.accounts.models import user,DoctorProfile
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from .models import Doctor_clinics

User = get_user_model()


class DoctorProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source="user.phone_number",write_only=True)
    profile_id = serializers.CharField(read_only=True)
    
    class Meta:
        model = DoctorProfile
        fields = ['profile_id',
                   'name', 
                   'registration_number', 
                   'registration_year',
                    'profile_image',
                    'description', 
                    'qualification',
                    'experience',
                    'phone_number'
                ]
    
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
    
    def create(self,validated_data):
        user = validated_data.pop("user")
        phone_number = self.initial_data.get("phone_number")
        with transaction.atomic():
            user.phone_number = phone_number
            user.save()
            doctor = DoctorProfile.objects.create(user = user,**validated_data)
        return doctor

class DoctorClincSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor_clinics
        fields = ['doctor','clinic','consultation_fee','consultation_duration'] 

    def validate(self, data):
        user = self.context['request'].user
        doctor = data.get('doctor')
        clinic = data.get('clinic')
        
        if Doctor_clinics.objects.filter(doctor=doctor, clinic=clinic).exists():
            raise serializers.ValidationError(
                {"detail": "This doctor is already assigned to this clinic."}
            )
        if user.user_role == "clinic_admin":
            if not clinic.admins.filter(id=user.id).exists():
                raise serializers.ValidationError(
                    {"detail": "You are not an admin of this clinic."}
                )

        if user.user_role == "receptionist":
            if not clinic.receptionists.filter(user_id=user.id).exists():
                raise serializers.ValidationError(
                    {"detail": "You are not a receptionist of this clinic."}
                )
        return data
    
    def create(self, validated_data):
        doctor_clinic = Doctor_clinics.objects.create(**validated_data)
        return doctor_clinic


class DoctorClinicInfoSerializer(serializers.ModelSerializer):
    clinic_name = serializers.CharField(source="clinic.name", read_only=True)
    clinic_address = serializers.CharField(source="clinic.address", read_only=True)
    clinic_city = serializers.CharField(source="clinic.city", read_only=True)

    class Meta:
        model = Doctor_clinics
        fields = [
            "id",
            "clinic",
            "clinic_name",
            "clinic_address",
            "clinic_city",
            "consultation_fee",
            "consultation_duration",
        ]


class DoctorListSerializer(serializers.ModelSerializer):
    clinics = DoctorClinicInfoSerializer(source="doctor_clinics", many=True, read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "profile_id",
            "name",
            "specialization",
            "qualification",
            "experience",
            "profile_image",
            "description",
            "consultation_duration",
            "consultation_fee",
            "is_active",
            "is_verified",
            "clinics",
        ]
