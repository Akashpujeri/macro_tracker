from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import FoodEntry, Goal, FoodTemplate, Entry

class MacroTrackerTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_dashboard_view_authenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")

    def test_food_entry_submission(self):
        response = self.client.post(reverse('dashboard'), {
            'food_name': 'Eggs',
            'calories': 155,
            'protein': 13,
            'carbs': 1,
            'fat': 11
        })
        self.assertEqual(response.status_code, 302)  # redirect after POST
        self.assertEqual(Entry.objects.count(), 1)

    def test_goal_setting(self):
        response = self.client.post(reverse('set_goal'), {
            'daily_calories': 2200,
            'protein_target': 120,
            'carb_target': 250,
            'fat_target': 70,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Goal.objects.count(), 1)
        goal = Goal.objects.get(user=self.user)
        self.assertEqual(goal.daily_calories, 2200)

    def test_food_template_creation(self):
        response = self.client.post(reverse('food_templates'), {
            'name': 'Oats',
            'calories': 300,
            'protein': 10,
            'carbs': 50,
            'fat': 5,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FoodTemplate.objects.count(), 1)
        template = FoodTemplate.objects.first()
        self.assertEqual(template.name, 'Oats')

    def test_invalid_entry(self):
        response = self.client.post(reverse('dashboard'), {
            'food_name': '',
            'calories': '',
            'protein': '',
            'carbs': '',
            'fat': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")
