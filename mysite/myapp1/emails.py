from django.core.mail import send_mail, send_mass_mail
import random
from .models import User
from django.conf import settings

def send_otp_via_email(email):
    subject= "your account verification email "
    otp= random.randint(1000,99999)
    message=f"your otp is {otp}"
    email_from= settings.EMAIL_HOST
    user= User.objects.get(email=email)
    user.otp=otp
    user.save()
    send_mail(subject,message,email_from,[email])

