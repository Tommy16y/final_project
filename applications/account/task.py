from celery import shared_task
from django.core.mail import send_mail
from decouple import config

@shared_task
def send_activation_code(email, code):
    send_mail(
        'Py25 project', # title
        f'http://localhost:8000/api/account/activate/{code}',# body
        config('EMAIL_ADRESS'), # from
        [email] # to
    )
