from django.urls import path
from .views import Craete_clinic_view
urlpatterns = [
    path('setup-clinic/',Craete_clinic_view.as_view(),name="create_clinic")
]