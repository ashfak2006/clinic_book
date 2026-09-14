from rest_framework import serializers
from apps.accounts.models import user,DoctorProfile
from phonenumber_field.serializerfields import PhoneNumberField

class DoctorProfileCreateSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region='IN', required=True,write_only=True)
    experience = serializers.IntegerField(required=False,min_value=0)
    qualification = serializers.CharField(required=False, max_length=255, allow_blank=True)
    registration_number = serializers.CharField(required=True, max_length=255)
    registration_year = serializers.IntegerField(required=True, min_value=1900, max_value=2100)
    description  = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    name = serializers.CharField(required=True, max_length=255)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    profile_id = serializers.CharField(required=False)
    
    def validate(self, attrs):
        
        return super().validate(attrs)
    def create(self, validated_data):
        return DoctorProfile.objects.create(**validated_data)

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['profile_id', 'name', 'registration_number', 'registration_year', 'profile_image', 'description', 'qualification', 'experience']
