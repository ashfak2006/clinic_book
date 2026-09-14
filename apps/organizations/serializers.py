from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Clinic
from apps.accounts.models import (user,ReceptionistProfile)
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

class Create_receptionist_serializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone_number = PhoneNumberField(required=True)
    password = serializers.CharField(required=True)
    profile_img = serializers.ImageField(required=False)
    def create(self, validated_data):
        user_obj = user(phone_number=validated_data.get('phone_number'),
                        email=validated_data.get("email"))
        user_obj.set_password(validated_data.get('password'))
        validated_data.pop('phone_number', None)
        validated_data.pop('email')
        validated_data.pop('password')
        with transaction.atomic():
            user_obj.save()
            res_obj = ReceptionistProfile.objects.create(user=user_obj,**validated_data)

        return res_obj