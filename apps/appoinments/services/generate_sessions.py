from datetime import timedelta
from ..models import ConsultationSession,TimeSlot
from django.utils import timezone


def generate_sessions(schedule, days=30):

    current_date = timezone.localdate()
    end_date = current_date + timedelta(days=days)

    date = current_date

    while date <= end_date:

        if date.weekday() == schedule.day_of_week:

            ConsultationSession.objects.get_or_create(

                doctor_clinic=schedule.doctor_clinic,

                date=date,

                defaults={

                    "start_time": schedule.start_time,

                    "end_time": schedule.end_time,

                    "time_slot": schedule,

                    "max_tokens": schedule.max_tokens,

                    "next_token_number": 1,

                }
            )

        date += timedelta(days=1)