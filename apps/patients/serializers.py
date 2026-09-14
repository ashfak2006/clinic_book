from rest_framework import serializers
from apps.accounts.models import PatientProfile

class patient_profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['name', 'profile_image', 'city', 'weight', 'height', 'state', 'country', 'date_of_birth']