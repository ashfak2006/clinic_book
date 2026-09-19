from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Doctor_clinics(models.Model):
    doctor = models.ForeignKey('accounts.DoctorProfile', on_delete=models.CASCADE, related_name='doctor_clinics')
    clinic = models.ForeignKey('organizations.Clinic', on_delete=models.CASCADE, related_name='clinic_doctors')
    consultation_duration = models.DurationField(null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    class Meta:
        unique_together = ('doctor', 'clinic')
    def __str__(self):
        return f"{self.doctor.name} - {self.clinic.name}-{self.id}"
    
class DoctorReview(models.Model):
    doctor = models.ForeignKey(
        'accounts.DoctorProfile', on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        'accounts.PatientProfile', on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=True)
    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "user"], name="unique_review_per_user_product"
            ),
            models.CheckConstraint(
                condition=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name="rating_between_1_and_5",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.doctor} ({self.rating}/5)"