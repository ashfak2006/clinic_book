from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse, OpenApiParameter
from rest_framework.pagination import PageNumberPagination
from apps.doctors.serializers import DoctorClincSerializer
from apps.accounts.permissions import IsClinicAdmin, IsReceptionist, IsClinicAdminOrReceptionist
from apps.doctors.models import Doctor_clinics
from apps.appoinments.models import TimeSlot, Appointment
from apps.appoinments.services import generate_sessions
from apps.appoinments.serializers import TimeSloteSerializer, AppointmentSerializer
from .models import Clinic
from .serializers import (
    ClinicCreateSerializer,
    ClinicDetailSerializer,
    ReceptionistCreateSerializer,
    ReceptionistProfileSerializer,
)


class ClinicCreateView(APIView):
    """
    Endpoint to register a new Clinic along with its Clinic Administrator account.
    """
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    @extend_schema(
        tags=["Organizations"],
        summary="Register a new Clinic and Clinic Administrator",
        description="Registers a new clinic alongside its clinic administrator user account.",
        request=ClinicCreateSerializer,
        responses={
            201: ClinicDetailSerializer,
            400: OpenApiResponse(description="Validation error."),
        },
    )
    def post(self, request):
        serializer = ClinicCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        clinic = serializer.save()
        output_serializer = ClinicDetailSerializer(clinic, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ReceptionistCreateView(APIView):
    """
    Endpoint for authenticated Clinic Administrators to register receptionists.
    """
    permission_classes = [permissions.IsAuthenticated, IsClinicAdmin]

    @extend_schema(
        tags=["Organizations"],
        summary="Register a receptionist for clinic",
        description="Endpoint for authenticated Clinic Administrators to register new receptionists.",
        request=ReceptionistCreateSerializer,
        responses={
            201: ReceptionistProfileSerializer,
            400: OpenApiResponse(description="Validation error or no clinic associated."),
        },
    )
    def post(self, request):
        clinic = Clinic.objects.filter(admin=request.user).first()
     
        if not clinic:
            return Response(
                {"detail": "No clinic associated with this administrator account."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ReceptionistCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            receptionist = serializer.save(clinic=clinic)

            output_serializer = ReceptionistProfileSerializer(receptionist, context={"request": request})
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateDoctorClinicView(APIView):
    """
    for creating connection between doctors and clinics
    """
    permission_classes = [permissions.IsAuthenticated, IsClinicAdminOrReceptionist]

    @extend_schema(
        tags=["Organizations"],
        summary="Assign doctor to clinic",
        description="Creates an association between a doctor and a clinic, specifying consultation fee and duration.",
        request=DoctorClincSerializer,
        responses={
            201: DoctorClincSerializer,
            400: OpenApiResponse(description="Validation error or unauthorized."),
        },
    )
    def post(self, request):
        serializer = DoctorClincSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            doctor_cliniic = serializer.save()
            output_serializer = DoctorClincSerializer(doctor_cliniic)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddTimeSloteview(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClinicAdminOrReceptionist]

    @extend_schema(
        tags=["Organizations"],
        summary="Add recurring time slot for doctor",
        description="Creates a recurring consultation time slot schedule for a doctor clinic assignment.",
        request=TimeSloteSerializer,
        responses={
            201: TimeSloteSerializer,
            400: OpenApiResponse(description="Validation error."),
        },
    )
    def post(self, request):
        serializer = TimeSloteSerializer(data=request.data)
        if serializer.is_valid():
            time_slote = serializer.save()
            output_serializer = TimeSloteSerializer(time_slote)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenerateSessions(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClinicAdminOrReceptionist]

    @extend_schema(
        tags=["Organizations"],
        summary="Generate consultation sessions from time slot",
        description="Generates daily consultation session instances for the specified upcoming number of days based on a recurring time slot.",
        request=inline_serializer(
            name="GenerateSessionsRequest",
            fields={
                "time_slot": serializers.IntegerField(help_text="ID of the TimeSlot schedule"),
                "days": serializers.IntegerField(default=30, required=False, help_text="Number of days ahead to generate sessions for"),
            },
        ),
        responses={
            201: OpenApiResponse(description="Consultation sessions generated successfully."),
            400: OpenApiResponse(description="Invalid request or TimeSlot not found."),
        },
    )
    def post(self, request):
        print(request)
        time_slot = request.data.get('time_slot')
        days = request.data.get('days', 30)
        shedule = TimeSlot.objects.get(id=time_slot)
        generate_sessions.generate_sessions(shedule, days=days)
        return Response(status=status.HTTP_201_CREATED)


class AppointmentPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class ClinicAppointmentListView(APIView):
    """
    Endpoint for Clinic Admins and Receptionists to list appointments for their clinic.
    Supports filtering by doctor (ID), status, and date.
    """
    permission_classes = [permissions.IsAuthenticated, IsClinicAdminOrReceptionist]
    pagination_class = AppointmentPagination

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
        tags=["Organizations"],
        summary="List clinic appointments",
        description="Lists appointments for the authenticated user's clinic. Filterable by doctor, status, and date.",
        parameters=[
            OpenApiParameter(
                name="doctor",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter appointments by doctor profile ID",
            ),
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter appointments by status (e.g. pending, confirmed, completed, cancelled)",
            ),
            OpenApiParameter(
                name="date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter appointments by session date (YYYY-MM-DD)",
            ),
        ],
        responses={
            200: AppointmentSerializer(many=True),
        },
    )
    def get(self, request):
        user = request.user
        clinic = None
        
        if getattr(user, 'user_role', None) == 'clinic_admin':
            if hasattr(user, 'clinc'):
                clinic = user.clinc
        elif getattr(user, 'user_role', None) == 'receptionist':
            if hasattr(user, 'receptionist_profile'):
                clinic = user.receptionist_profile.clinic
                
        if not clinic:
            return Response(
                {"detail": "No clinic associated with this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = (
            Appointment.objects.filter(session__doctor_clinic__clinic=clinic)
            .order_by("-created_at")
            .select_related("patient", "session", "session__doctor_clinic")
        )

        doctor_id = request.query_params.get("doctor")
        appointment_status = request.query_params.get("status")
        session_date = request.query_params.get("date")

        if doctor_id:
            queryset = queryset.filter(session__doctor_clinic__doctor_id=doctor_id)
        if appointment_status:
            queryset = queryset.filter(status=appointment_status)
        if session_date:
            queryset = queryset.filter(session__date=session_date)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AppointmentSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = AppointmentSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)



