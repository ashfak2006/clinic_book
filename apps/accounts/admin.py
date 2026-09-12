from django.contrib import admin
from .models import user, City, DoctorProfile, ReceptionistProfile

admin.site.register(user)
admin.site.register(City)
admin.site.register(DoctorProfile)
admin.site.register(ReceptionistProfile)

# Register your models here.
