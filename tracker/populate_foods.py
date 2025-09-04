from tracker.models import FoodDatabase
import csv
import os

def run():
    with open(os.path.join(os.path.dirname(__file__), 'food_data.csv')) as file:
        reader = csv.DictReader(file)
        for row in reader:
            FoodDatabase.objects.create(
                name=row['name'],
                calories=float(row['calories']),
                protein=float(row['protein']),
                carbs=float(row['carbs']),
                fat=float(row['fat'])
            )
