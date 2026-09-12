from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)
    _state = [('Andhra Pradesh', 'Andhra Pradesh'),
              ('Arunachal Pradesh', 'Arunachal Pradesh'),
              ('Assam', 'Assam'),
              ('Bihar', 'Bihar'),
              ('Chhattisgarh', 'Chhattisgarh'),
              ('Goa', 'Goa'),
              ('Gujarat', 'Gujarat'),
              ('Haryana', 'Haryana'),
              ('Himachal Pradesh', 'Himachal Pradesh'),
              ('Jharkhand', 'Jharkhand'),
              ('Karnataka', 'Karnataka'),
              ('Kerala', 'Kerala'),
              ('Madhya Pradesh', 'Madhya Pradesh'),
              ('Maharashtra', 'Maharashtra'),
              ('Manipur', 'Manipur'),
              ('Meghalaya', 'Meghalaya'),
              ('Mizoram', 'Mizoram'),
              ('Nagaland', 'Nagaland'),
              ('Odisha', 'Odisha'),
              ('Punjab', 'Punjab'),
              ('Rajasthan', 'Rajasthan'),
              ('Sikkim', 'Sikkim'),
              ('Tamil Nadu', 'Tamil Nadu'),
              ('Telangana', 'Telangana'),
              ('Tripura', 'Tripura'),
              ('Uttar Pradesh', 'Uttar Pradesh'),
              ('Uttarakhand', 'Uttarakhand'),
              ('West Bengal', 'West Bengal')]
    state = models.CharField(max_length=100, choices=_state)
    country = models.CharField(max_length=100, default='india')

    def __str__(self):
        return f"{self.name}, {self.state}, {self.country}"

class user(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True,blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True,unique=True)
    user_role = models.CharField(max_length=50, choices=[('doctor', 'Doctor'),
                                                          ('patient', 'Patient'),
                                                          ('receptionist', 'Receptionist'),
                                                          ('admin', 'Admin'),
                                                          ('clinic_admin', 'Clinic Admin')
                                                          ], default='patient')

    def __str__(self):
        return self.username

class DoctorProfile(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='doctor_profile')
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='media/doctor_profiles/', null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    qualification = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    consultation_duration = models.DurationField(null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} user {self.user.email}"

class PatientProfile(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='patient_profile')
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='media/patient_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=100, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, default='india')
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} user {self.user.email}"

class ReceptionistProfile(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='receptionist_profile')
    name = models.CharField(max_length=100)
    clinic = models.ForeignKey('organizations.Clinic', on_delete=models.CASCADE, null=True, blank=True, related_name='receptionists')
    profile_image = models.ImageField(upload_to='media/receptionist_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} user {self.user.email}"

class AdminProfile(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='admin_profile')
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='media/admin_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} user {self.user.email}"