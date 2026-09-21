from django.urls import path
from .views import (DoctorListView, DoctorProfileViewSet,ListSpecialisationsView,
                    ListDoctorAppoinmentsView,ListDoctorClinicsView)

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctor-profile/', DoctorProfileViewSet.as_view(), name='doctor-profile'),
    path("specialisations/", ListSpecialisationsView.as_view(), name="specialisations"),
    path('doctor-list-appoinments',ListDoctorAppoinmentsView.as_view(),name='lis_appoinment_for doctor'),
    path('doctor-list-clinics',ListDoctorClinicsView.as_view(),name="list_doctors_clinics")
]
