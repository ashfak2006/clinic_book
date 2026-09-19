from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from apps.accounts.permissions import IsPatient
from apps.accounts.models import PatientProfile
from .serializers import patient_profile_serializer


class PatientAccountCreate(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPatient]
    serializer_class = patient_profile_serializer

    @extend_schema(
        tags=["Patients"],
        summary="Retrieve Patient Profile",
        description="Retrieves the profile of the currently authenticated patient.",
        responses={
            200: inline_serializer(
                name="PatientProfileResponse",
                fields={
                    "message": serializers.CharField(default="Patient profile retrieved successfully."),
                    "user": patient_profile_serializer(),
                },
            ),
            404: OpenApiResponse(description="User or patient profile not found."),
        },
    )
    def get(self, request):
        user_obj = request.user
        if not user_obj:
            return Response({'error': 'User not found.'}, status=404)
        if hasattr(user_obj, 'patientprofile'):
            serializer = self.serializer_class(user_obj.patientprofile)
            return Response({'message': 'Patient profile retrieved successfully.', 'user': serializer.data}, status=200)
        else:
            return Response({'error': 'Patient profile not found.'}, status=404)

    @extend_schema(
        tags=["Patients"],
        summary="Setup Patient Profile",
        description="Sets up the patient profile and updates phone number for the authenticated patient.",
        request=inline_serializer(
            name="PatientAccountSetupRequest",
            fields={
                "name": serializers.CharField(max_length=100, required=True),
                "phone_number": serializers.CharField(required=False, allow_blank=True),
                "profile_image": serializers.ImageField(required=False, allow_null=True),
                "city": serializers.CharField(max_length=100, required=False, allow_blank=True),
                "weight": serializers.FloatField(required=False, allow_null=True),
                "height": serializers.FloatField(required=False, allow_null=True),
                "state": serializers.CharField(max_length=100, required=False, allow_blank=True),
                "country": serializers.CharField(max_length=100, required=False, allow_blank=True),
                "date_of_birth": serializers.DateField(required=False, allow_null=True),
            },
        ),
        responses={
            200: inline_serializer(
                name="PatientAccountSetupSuccessResponse",
                fields={
                    "message": serializers.CharField(default="Account setup successfully."),
                    "user": patient_profile_serializer(),
                },
            ),
            400: OpenApiResponse(description="Account already setup or validation error."),
            404: OpenApiResponse(description="User not found."),
        },
    )
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