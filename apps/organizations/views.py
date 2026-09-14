from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from rest_framework import permissions
from rest_framework.response import Response
from apps.accounts.permissions import (
    IsClinicAdmin,
    IsAdmin
)
from apps.accounts.models import(
    user
)
from .models import Clinic
from .serializers import (Create_clinic_serializer,
                          Create_receptionist_serializer
                          )
from rest_framework.views import APIView

class Craete_clinic_view(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        serializer = Create_clinic_serializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)
    
class Create_reseptionist_view(APIView):
    permission_classes= [permissions.IsAuthenticated,IsClinicAdmin]
    def post(self,request):
        serializer = Create_receptionist_serializer(data=request.data)
        clinic_obj = Clinic.objects.get(admin=request.user)
        if serializer.is_valid():
            serializer.save(clinic=clinic_obj)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)

        
        
        


