from django.contrib import admin
from .models import user, City, DoctorProfile, ReceptionistProfile,PatientProfile

admin.site.register(user)
admin.site.register(City)
admin.site.register(DoctorProfile)
admin.site.register(ReceptionistProfile)
admin.site.register(PatientProfile)


# Register your models here.
