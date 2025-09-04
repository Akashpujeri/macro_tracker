from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Entry
from datetime import date

@shared_task
def send_daily_reminders():
    users = User.objects.all()
    for user in users:
        has_logged = Entry.objects.filter(user=user, date=date.today()).exists()
        if not has_logged and user.email:
            send_mail(
                subject='🍽️ Reminder: Log Your Meals Today!',
                message=f"Hi {user.username},\n\nYou haven’t logged any meals today. Don’t forget to track your nutrition!",
                from_email='no-reply@macrotracker.com',
                recipient_list=[user.email],
                fail_silently=True
            )
