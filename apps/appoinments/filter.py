import django_filters
from .models import Appointment

class AppointmentFilter(django_filters.FilterSet):
    clinic_id = django_filters.NumberFilter(field_name="session__doctor_clinic__clinic__id")
    clinic_name = django_filters.CharFilter(field_name="session__doctor_clinic__clinic__name", lookup_expr='icontains')

    class Meta:
        model = Appointment
        fields = ['clinic_id', 'clinic_name','session','status']