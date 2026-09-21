from django.contrib import admin

from .models import Doctor_clinics,Specialisations

# Register your models here.
admin.site.register(Doctor_clinics)
admin.site.register(Specialisations)