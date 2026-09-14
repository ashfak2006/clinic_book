from django.core.mail import send_mail

class EmailService:
    @staticmethod
    def send_email(subject, body, to_email):
        send_mail(
            subject,
            body,
            'settings.EMAIL_HOST_USER',
            [to_email],
            fail_silently=False,
        )