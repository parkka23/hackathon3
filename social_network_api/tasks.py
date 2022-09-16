from .celery import app
from account.send_email import send_confirmation_email


@app.task
def send_email_task(to_email, code):
    send_confirmation_email(to_email, code)
