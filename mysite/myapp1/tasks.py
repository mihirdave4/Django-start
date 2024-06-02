# myapp/tasks.py
from datetime import timedelta
from django.utils import timezone
from background_task import background

@background(schedule=timedelta(minutes=5))
def erase_expired_otps():
    from .models import User  # Import your User model
    cutoff_time = timezone.now() - timedelta(minutes=5)  # Adjust the time limit as needed

    # Delete OTPs older than the cutoff time
    User.objects.filter(otp__lt=cutoff_time).update(otp=None)
