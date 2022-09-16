from django.core.mail import send_mail


def send_confirmation_email(user):
    code = user.activation_code
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}/'
    to_email = user.email
    send_mail(
        'Hello, activate your account.',
        f'Follow the link to activate your account: {full_link}',
        'park.ksenia23@gmail.com',
        [to_email, ],
        fail_silently=False
    )


def send_reset_password(user):
    code = user.activation_code
    to_email = user.email
    send_mail(
        'Subject',
        f'Password recovery code: {code}',
        'from@example.com',
        [to_email, ],
        fail_silently=False
    )
