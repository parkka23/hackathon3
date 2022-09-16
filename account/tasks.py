from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from social_network_api import settings
from time import sleep


@shared_task(bind=True)
def send_spam_task(self, duration):
    sleep(duration)
    users = get_user_model().objects.all()
    for user in users:
        mail_subject = "Hi! Spam from Social Network!"
        message = "Do you like using our Social Network? Then share it with your friends and have a good time together!"
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False,
        )
    return "Spam email task done"


@shared_task(bind=True)
def send_login_mail_task(self, email):
    sleep(5)
    mail_subject = "Notification from Social Network"
    message = "You successfully logged in."
    to_email = email
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
    return "Login notification email sent"


@shared_task(bind=True)
def send_logout_mail_task(self, email):
    sleep(5)
    mail_subject = "Notification from Social Network"
    message = "You successfully logged out."
    to_email = email
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
    return "Logout notification email sent"
