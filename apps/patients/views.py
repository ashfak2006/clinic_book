from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from apps.accounts.permissions import IsPatient
from apps.accounts.models import PatientProfile
from .serializers import patient_profile_serializer
# Create your views here.

class PatientAccountCreate(APIView):
    permission_classes = [permissions.IsAuthenticated,IsPatient]
    serializer_class = patient_profile_serializer
    def get(self, request):
        user_obj = request.user
        if not user_obj:
            return Response({'error': 'User not found.'}, status=404)
        if hasattr(user_obj, 'patientprofile'):
            serializer = self.serializer_class(user_obj.patientprofile)
            return Response({'message': 'Patient profile retrieved successfully.', 'user': serializer.data}, status=200)
        else:
            return Response({'error': 'Patient profile not found.'}, status=404)
    def post(self, request):
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        user_obj = request.user
        if user_obj.phone_number and hasattr(user_obj, 'patientprofile'):
            return Response({'error': 'Account already setup.'}, status=400)
        if not user_obj:
            return Response({'error': 'User not found.'}, status=404)
        user_obj.phone_number = phone_number
        patient_profile = PatientProfile(user=user_obj, name=name)
        serializer = self.serializer_class(patient_profile, data=request.data, partial=True)
        if serializer.is_valid():
            user_obj.save()
            serializer.save()
            return Response({'message': 'Account setup successfully.', 'user': serializer.data}, status=200)
        return Response(serializer.errors, status=400)