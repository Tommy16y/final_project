from django.core.mail import send_mail
from decouple import config
def send_activation_code(email, code):
    send_mail(
        'Py25 project', # title
        f'http://localhost:8000/api/account/activate/{code}', # body
        config('EMAIL_ADRESS'), # from
        [email] # to
    )
# 35.234.109.231
def send_reset_password_code(email, code):
    send_mail(
        'Py25 project', # title
        f'привет чтобы бросить пароль тебе нужно знать этот код = {code}', # body
        config('EMAIL_ADRESS'), # from
        [email] # to
    )