from django.shortcuts import render
from apps.accounts.models import user,DoctorProfile
from rest_framework import generics, permissions
from rest_framework.response import Response
from apps.accounts.permissions import IsDoctor
from .serializers import (DoctorProfileCreateSerializer, 
                            DoctorProfileSerializer
                        )
# Create your views here.

class DoctorProfileViewSet(generics.ListCreateAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DoctorProfileCreateSerializer
        return DoctorProfileSerializer
    def get_queryset(self):
        return DoctorProfile.objects.filter(user=self.request.user,is_active=True).first()
    def get(self,request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response({'doctor_profile': serializer.data}, status=200)
        else:
            return Response({'error': 'Doctor profile not found.'}, status=404)
        
    def perform_create(self,serializer):
        user = self.request.user
        if serializer.validated_data.get("phone_number"):
            phone_number = serializer.validated_data.get("phone_number")
            user.phone_number = phone_number
            user.save()
        if DoctorProfile.objects.filter(user=user).exists():
            return Response({'error': 'Doctor profile already exists for this user.'}, status=400)
        
        serializer.save(user=user)
        return Response({'message': 'Doctor profile created successfully.'}, status=201)