from django.contrib import admin
from .models import Appointment, TimeSlot, ConsultationSession, AvailabilityException
# Register your models here.
admin.site.register(Appointment)
admin.site.register(TimeSlot)
admin.site.register(ConsultationSession)
admin.site.register(AvailabilityException)
