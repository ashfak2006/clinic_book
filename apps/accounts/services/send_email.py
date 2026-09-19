import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class EmailService:
    @staticmethod
    def send_email(subject: str, body: str, to_email: str) -> bool:
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", getattr(settings, "EMAIL_HOST_USER", "noreply@clinicbook.com"))
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=from_email,
                recipient_list=[to_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, str(e))
            return False