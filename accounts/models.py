from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly Active'),
        ('moderate', 'Moderately Active'),
        ('active', 'Active'),
        ('very_active', 'Very Active'),
    ]
    
    GOAL_CHOICES = [
        ('lose', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain', 'Gain Muscle'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile') 
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    weight = models.FloatField(help_text="In kilograms", null=True, blank=True)
    height = models.FloatField(help_text="In centimeters", null=True, blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, null=True, blank=True)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
