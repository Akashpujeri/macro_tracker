from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import api_views

urlpatterns = [
    path('', views.home, name='home'),  
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('ajax/food-search/', views.food_search, name='food_search'), 
    
    path('set-goals/', views.set_goals, name='set_goals'),
    path('food-templates/', views.food_templates, name='food_templates'),
    path('food-templates/delete/<int:template_id>/', views.delete_template, name='delete_template'),
    path('edit-template/<int:template_id>/', views.edit_template, name='edit_template'),

    path('articles/', views.article_list, name='article_list'),
    path('create-article/', views.create_article, name='create_article'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),

    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),

    # API endpoints
    path('api/food-entries/', api_views.FoodEntryListCreateView.as_view(), name='api_food_entries'),
    path('api/goals/', api_views.GoalRetrieveUpdateView.as_view(), name='api_goals'),
    path('api/templates/', api_views.FoodTemplateListCreateView.as_view(), name='api_templates'),

    path('activity-calendar/', views.activity_calendar_view, name='activity_calendar'),  
    path('daily-activity/<str:date_str>/', views.daily_activity, name='daily_activity'),
    path('calendar/', views.calendar_view, name='calendar_view'),

]
