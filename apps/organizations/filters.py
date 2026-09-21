from  django_filters import FilterSet
from .models import Clinic

class ClinicFilter(FilterSet):
    class Meta:
        model = Clinic
        fields = [
                    "id",
                    "name",
                    "city",
                    "is_verified",
                    "is_active"
                    ]