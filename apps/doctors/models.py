from django.db import models

# Create your models here.
class Doctor_clinics(models.Model):
    doctor = models.ForeignKey('accounts.DoctorProfile', on_delete=models.CASCADE, related_name='doctor_clinics')
    clinic = models.ForeignKey('organizations.Clinic', on_delete=models.CASCADE, related_name='clinic_doctors')
    consultation_duration = models.DurationField(null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    class Meta:
        unique_together = ('doctor', 'clinic')
    def __str__(self):
        return f"{self.doctor.name} - {self.clinic.name}"