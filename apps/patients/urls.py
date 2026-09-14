from django.urls import path,include
from .views import(PatientAccountCreate)

urlpatterns = [
    path('user-account/',PatientAccountCreate.as_view(),name='user-account-setup')
]