from django.contrib import admin
from .models import Article, FoodDatabase
from accounts.models import UserProfile 

from django_celery_beat.models import PeriodicTask, IntervalSchedule
admin.site.register(Article)

admin.site.register(FoodDatabase)
admin.site.register(UserProfile)

