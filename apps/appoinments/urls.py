from django.urls import path
from .views import AppointmentCreateView

urlpatterns = [
    path("book/", AppointmentCreateView.as_view(), name="book_appointment"),
]
