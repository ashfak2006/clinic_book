from django.urls import path
from .views import Craete_clinic_view,Create_reseptionist_view
urlpatterns = [
    path('setup-clinic/',Craete_clinic_view.as_view(),name="create_clinic"),
    path('create-reseptionist/',Create_reseptionist_view.as_view(),name="create_reseptionist")
]