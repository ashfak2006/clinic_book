import datetime
from django.db import models
from django.db.models import Q, F

# Create your models here.
class TimeSlot(models.Model):
    class LocationType(models.TextChoices):
        CLINIC = "CLINIC", "Clinic"
        ONLINE = "ONLINE", "Online"
        CUSTOM = "CUSTOM", "Custom"
    start_time = models.TimeField()
    end_time = models.TimeField()
    doctor_clinic = models.ForeignKey('doctors.Doctor_clinics',on_delete=models.CASCADE,related_name='available_slots')
    doctor = models.ForeignKey('accounts.DoctorProfile', on_delete=models.CASCADE, related_name='available_slots')
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

    class Meta:
        constraints = [
            models.CheckConstraint(
            condition=Q(
                end_time__gt=F("start_time")
            ),
            name="availability_end_after_start"
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "doctor",
                    "day_of_week",
                    "is_active"
                ]
            )
        ]

class Appointment(models.Model):
    patient = models.ForeignKey('accounts.PatientProfile', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('accounts.DoctorProfile', on_delete=models.CASCADE, related_name='appointments')
    clinic = models.ForeignKey('organizations.Clinic', on_delete=models.CASCADE, null=True, blank=True, related_name='appointments')
    status_choices = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    appointment_date = models.DateField()
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='appointments')
    reason_for_visit = models.TextField(blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status_choices = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]
    payment_status = models.CharField(max_length=10, choices=payment_status_choices, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment: {self.patient} with {self.doctor} at {self.clinic} on {self.appointment_date} {self.timeslot}"

    
    class Meta:
        constraints = [
            models.CheckConstraint(
            condition=Q(
                appointment_date__lt=F("created_at__date")
            ),
            name="appointment_date_in_future"
            ),
        ]