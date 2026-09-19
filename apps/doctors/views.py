from django.shortcuts import render
from apps.accounts.models import user, DoctorProfile
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from apps.accounts.permissions import IsDoctor, IsClinicAdmin, IsReceptionist
from .serializers import DoctorListSerializer, DoctorProfileSerializer


class DoctorPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class DoctorListView(APIView):
    """
    Public endpoint for listing doctors.
    """
    permission_classes = [permissions.AllowAny]
    pagination_class = DoctorPagination
    throttle_classes = [AnonRateThrottle]

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    @extend_schema(
        tags=["Doctors"],
        summary="List all doctors",
        description="Public endpoint to list active doctors with pagination. Supports optional filtering by specialization, clinic ID, and search by doctor name.",
        parameters=[
            OpenApiParameter(
                name="specialization",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter doctors by specialization",
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Search doctors by name",
            ),
            OpenApiParameter(
                name="clinic",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter doctors by clinic ID",
            ),
        ],
        responses={
            200: DoctorListSerializer(many=True),
        },
    )
    def get(self, request):
        queryset = (
            DoctorProfile.objects.filter(is_active=True)
            .order_by("id")
            .prefetch_related("doctor_clinics__clinic")
        )
        specialization = request.query_params.get("specialization")
        search = request.query_params.get("search")
        clinic_id = request.query_params.get("clinic")

        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if clinic_id:
            queryset = queryset.filter(doctor_clinics__clinic_id=clinic_id).distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DoctorListSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = DoctorListSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorProfileViewSet(APIView):
    """
    for doctors after login 
    """
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        tags=["Doctors"],
        summary="Retrieve Doctor Profile",
        description="Retrieves profile information for the authenticated doctor.",
        responses={
            200: DoctorProfileSerializer,
            400: OpenApiResponse(description="Doctor profile not found."),
        },
    )
    def get(self, request, *args, **kwargs):
        user = self.request.user
        Doctor = DoctorProfile.objects.filter(user=user).first()
        if Doctor:
            output_doctor = DoctorProfileSerializer(Doctor, context={"request": request})
            return Response(output_doctor.data, status=status.HTTP_200_OK)
        return Response({"error": "doctor note found"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["Doctors"],
        summary="Create Doctor Profile",
        description="Creates a new doctor profile with qualification, experience, registration details, and profile image.",
        request=DoctorProfileSerializer,
        responses={
            201: DoctorProfileSerializer,
            400: OpenApiResponse(description="Validation error or profile already exists."),
        },
    )
    def post(self, request):
        user = request.user
       
        if DoctorProfile.objects.filter(user=user).exists():
            return Response({'error': 'Doctor profile already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DoctorProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Doctor = serializer.save(user=user)
        output_serializer = DoctorProfileSerializer(Doctor, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

       
