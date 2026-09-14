from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Clinic
from apps.accounts.models import user
from django.db import transaction
class Create_clinic_serializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    address = serializers.CharField()
    location = serializers.URLField()
    city = serializers.CharField()
    password = serializers.CharField(required=False)
    calling_number = PhoneNumberField(required=False)

    def validate(self, attrs):
        return super().validate(attrs)
    def create(self, validated_data):
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        user_obj = user(email=email,phone_number=phone_number,user_role='clinic_admin')
        if validated_data.get('password'):
            password = validated_data.get('password')
            user_obj.set_password(password)
        with transaction.atomic():
            user_obj.save()
            validated_data.pop("password")
            clinic_ob = Clinic.objects.create(admin=user_obj,**validated_data)
        return clinic_ob
        