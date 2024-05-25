from django.core.mail import send_mail
from main.celery import app

@app.task
def send_act_code_celery(email, code):
    link = f'http://localhost:8000/api/v1/account/confirm/{code}/'
    send_mail(
        'Ваш код для активации аккаунта',
        f'Здрвствуйте {email}, нажмите на данную ссылку для активации вашего аккаунта: \n {link}',
        'ulanovulukbek2@gmail.com',
        [email]    
    )
    
    
@app.task    
def send_confirmation_code(email, code):
    send_mail(
        'Код для восстановления пароля',
        f'Здравствуйте {email}, скопируйте этот код для восстановления пароля: \n{code}',
        'ulanovulukbek2 @gmail.com',
        [email],
    )