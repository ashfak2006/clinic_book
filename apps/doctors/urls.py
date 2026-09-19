from django.urls import path
from .views import DoctorListView, DoctorProfileViewSet

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctor-profile/', DoctorProfileViewSet.as_view(), name='doctor-profile'),
]