from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_activation_code(email, code):
    send_mail(
        'Py25 shop project', # title
        f'http://localhost:8000/api/account/activate/{code}', # body
        'imanaliev479125@gmail.com', # from
        [email] # to
    )