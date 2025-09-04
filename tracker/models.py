from django.db import models
from django.contrib.auth.models import User

class FoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    food_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.IntegerField()
    carbs = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return f"{self.food_name} ({self.date})"

class Goal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    calorie_goal = models.FloatField(default=2000)
    protein_goal = models.FloatField(default=50)
    carb_goal = models.FloatField(default=250)
    fat_goal = models.FloatField(default=70)

    def __str__(self):
        return f"{self.user.username}'s Goal"
    
class FoodTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.IntegerField()
    carbs = models.IntegerField()
    fat = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class FoodDatabase(models.Model): 
    name = models.CharField(max_length=100)
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)   

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
