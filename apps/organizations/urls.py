from django.urls import path
from .views import (ClinicCreateView, ReceptionistCreateView,
                    CreateDoctorClinicView, AddTimeSloteview,
                    GenerateSessions, ClinicAppointmentListView,
                    UpdateAppoinmentStatus)

urlpatterns = [
    path("setup-clinic/", ClinicCreateView.as_view(), name="create_clinic"),
    path("create-receptionist/", ReceptionistCreateView.as_view(), name="create_receptionist"),
    path("create-doctor-clinic/",CreateDoctorClinicView.as_view(),name="add_doctor_clinic"),
    path("add-timeslote/",AddTimeSloteview.as_view(),name='add_timeslote'),
    path('generate-sessions/',GenerateSessions.as_view(),name='generate-sessions'),
    path('appointments/', ClinicAppointmentListView.as_view(), name='clinic_appointments'),
    path('update-appointment-status/<int:pk>',UpdateAppoinmentStatus.as_view(),name='edit_appoinment_status')
]