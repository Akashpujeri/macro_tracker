from rest_framework import serializers
from .models import FoodEntry, Goal, FoodTemplate

class FoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodEntry
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class FoodTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTemplate
        fields = '__all__'
