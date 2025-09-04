from django import forms
from .models import FoodEntry, Goal, FoodTemplate, Article
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['date','food_name','calories','protein','carbs','fat']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class FoodTemplateForm(forms.ModelForm):
    class Meta:
        model = FoodTemplate
        fields = ['name','calories','protein','fat','carbs']

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['calorie_goal', 'protein_goal', 'carb_goal', 'fat_goal']

        def __init__(self, *args, **kwargs):
            self.daily_limit = kwargs.pop('daily_limit', None)
            super().__init__(*args, **kwargs)

    def clean_calories(self):
        calories = self.cleaned_data.get('calories')
        if self.daily_limit and calories > self.daily_limit:
            raise forms.ValidationError(f"⚠️ Calories exceed your daily limit of {self.daily_limit}.")
        return calories

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
