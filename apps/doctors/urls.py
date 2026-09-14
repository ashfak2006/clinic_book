from django.urls import path, include
from .views import DoctorProfileViewSet

urlpatterns = [
    path('doctor-profile/', DoctorProfileViewSet.as_view(), name='doctor-profile'),
]