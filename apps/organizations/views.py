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
from .serializers import Create_clinic_serializer
from rest_framework.views import APIView

class Craete_clinic_view(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        serializer = Create_clinic_serializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)
       
        
        
        


