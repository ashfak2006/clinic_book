from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiResponse
from apps.accounts.permissions import IsPatient
from django.db.models import Q
from .models import ConsultationSession, Appointment
from .serializers import AppointmentCreateSerializer, AppointmentSerializer

class AppointmentCreateView(generics.CreateAPIView):
    """
    Endpoint for patients to book an appointment for a consultation session.
    """
    permission_classes = [permissions.IsAuthenticated, IsPatient]
    serializer_class = AppointmentCreateSerializer

    @extend_schema(
        tags=["Appointments"],
        summary="Book an appointment",
        description="Allows a patient to book an appointment for a specific consultation session. Auto-assigns token number and calculates fee.",
        responses={
            201: AppointmentSerializer,
            400: OpenApiResponse(description="Validation error, session full, or session inactive."),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.validated_data.get('session')
        patient = getattr(request.user, 'patient_profile', None)

        if not patient:
            return Response({"detail": "User is not registered as a patient."}, status=status.HTTP_400_BAD_REQUEST)

        if not session.is_active:
            return Response({"detail": "This consultation session is no longer active."}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            session = ConsultationSession.objects.select_for_update().get(id=session.id)
            
            if session.next_token_number > session.max_tokens:
                return Response({"detail": "This session is fully booked."}, status=status.HTTP_400_BAD_REQUEST)
            
            if Appointment.objects.filter(Q(status='pending') | Q(status='confirmed'),session=session, patient=patient).exists():
                return Response({"detail": "You have already booked an appointment for this session."}, status=status.HTTP_400_BAD_REQUEST)

            token_number = session.next_token_number
            fee = session.doctor_clinic.consultation_fee
            
            appointment = Appointment.objects.create(
                patient=patient,
                session=session,
                reason_for_visit=serializer.validated_data.get('reason_for_visit', ''),
                fee=fee,
                token_number=token_number,
                status='pending',
                payment_status='unpaid'
            )
            
            session.next_token_number += 1
            session.save(update_fields=['next_token_number'])

        output_serializer = AppointmentSerializer(appointment, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
