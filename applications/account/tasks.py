from django.core.mail import send_mail
from main.celery import app

@app.task
def send_confirmation_email(email, code):
    full_link = f'http://127.0.0.1:8000/api/v1/account/confirm/{code}'
    send_mail(
        'User activation',
        f'Please, click the link to acitvate profile:  {full_link}',
        'ulanoffulukbek@yandex.ru',
        [email]
    )


@app.task
def send_confirmation_code(email, code):
    send_mail(
        'Password recovery',
        f'Please, enter code to recover profile password: {code}',
        'ulanoffulukbek@yandex.ru',
        [email]
    )