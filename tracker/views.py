from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import  UserCreationForm
from django.contrib import messages
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import UserProfile

from .models import FoodEntry, Goal, FoodTemplate, Article, FoodDatabase
from .forms import FoodEntryForm, GoalForm, FoodTemplateForm, ArticleForm

from datetime import date, timedelta, datetime
from django.utils import timezone
from django.utils.timezone import now
from collections import defaultdict

from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, 'tracker/home.html')

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('dashboard')
    else:
        form = FoodEntryForm()

    # Get entries
    entries = FoodEntry.objects.filter(user=request.user).order_by('-date')
    totals = entries.aggregate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein'),
        total_carbs=Sum('carbs'),
        total_fat=Sum('fat')
    )
    templates = FoodTemplate.objects.filter(user=request.user)

    # Goal check
    try:
        goal = Goal.objects.get(user=request.user)
        recommended_limit = 2000
        if goal.calorie_goal > recommended_limit:
            messages.warning(request, "⚠️ Your calorie goal exceeds the recommended daily limit!")
    except Goal.DoesNotExist:
        goal = None

    # --- 🔥 STREAK SYSTEM ---
    today = now().date()
    streak = 0
    for i in range(0, 100):  # max 100 days streak
        check_date = today - timedelta(days=i)
        if FoodEntry.objects.filter(user=request.user, date=check_date).exists():
            streak += 1
        else:
            break  # streak broken

    context = {
        'form': form,
        'entries': entries,
        'totals': totals,
        'templates': templates,
        'goal': goal,
        'streak_count': streak,
    }

    return render(request, 'tracker/dashboard.html', context)



from django.http import JsonResponse
from .models import FoodDatabase

def food_search(request):
    term = request.GET.get('term', '')
    foods = FoodDatabase.objects.filter(name__icontains=term)[:10]
    results = [
        {
            "label": f"{f.name} ({f.calories} kcal)",
            "value": f.name,
            "calories": f.calories,
            "protein": f.protein,
            "carbs": f.carbs,
            "fat": f.fat,
        }
        for f in foods
    ]
    return JsonResponse(results, safe=False)

def update_macro_streak(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    today = date.today()

    if profile.last_logged_date == today:
        return  # already logged
    elif profile.last_logged_date == today - timedelta(days=1):
        profile.macro_streak += 1
    else:
        profile.macro_streak = 1  # reset streak

    profile.last_logged_date = today
    profile.save()

def log_food(request):
    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            # Save entry logic here (optional for your model)
            update_macro_streak(request.user)
            streak = request.user.userprofile.macro_streak
            messages.success(request, f"You’ve hit your macros {streak} days in a row! 🔥")
            return redirect('dashboard')

@login_required
def set_goals(request):
    goal = Goal.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('dashboard')
    else:
        form = GoalForm(instance=goal)

    return render(request, 'tracker/set_goals.html', {'form': form})

@login_required
def food_templates(request):
    templates = FoodTemplate.objects.filter(user=request.user)
    form = FoodTemplateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        template = form.save(commit=False)
        template.user = request.user
        template.save()
        messages.success(request, "Template saved successfully!")
        return redirect('food_templates')

    return render(request, 'tracker/food_templates.html', {
        'form': form,
        'templates': templates
    })

@login_required
def delete_template(request, template_id):
    template = get_object_or_404(FoodTemplate, id=template_id, user=request.user)
    template.delete()
    messages.success(request, "Template deleted successfully!")
    return redirect('food_templates')

@login_required
def edit_template(request, template_id):
    template = get_object_or_404(FoodTemplate, id=template_id, user=request.user)

    if request.method == 'POST':
        form = FoodTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect('food_templates')
    else:
        form = FoodTemplateForm(instance=template)

    return render(request, 'tracker/edit_template.html', {'form': form})

@staff_member_required
def create_article(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save()
        messages.success(request, "Article published.")
        return redirect('articles')
    return render(request, 'tracker/create_article.html', {'form': form})

def article_list(request):
    articles = Article.objects.all().order_by('-published_date')
    return render(request, 'tracker/article_list.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'tracker/article_detail.html', {'article': article})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(FoodEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = FoodEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Entry updated successfully!")
            return redirect('daily_activity', date_str=entry.date.strftime('%Y-%m-%d'))
    else:
        form = FoodEntryForm(instance=entry)
    return render(request, 'tracker/edit_entry.html', {'form': form})


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(FoodEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry_date = entry.date.strftime('%Y-%m-%d')
        entry.delete()
        messages.success(request, "Entry deleted successfully.")
        return redirect('daily_activity', date_str=entry_date)
    return render(request, 'tracker/confirm_delete.html', {'entry': entry})

@login_required
def activity_calendar_view(request):
    today = timezone.now().date()
    start_date = today.replace(day=1)

    entries = FoodEntry.objects.filter(user=request.user, date__month=start_date.month)

    day_totals = defaultdict(int)
    for entry in entries:
        day_totals[entry.date] += entry.calories

    current = start_date
    days = []
    while current.month == start_date.month:
        days.append({
            'date': current,
            'calories': day_totals.get(current, 0)
        })
        current += timedelta(days=1)

    return render(request, 'tracker/activity_calendar.html', {
        'days': days,
        'month': start_date.strftime('%B %Y')
    })


def daily_activity(request, date_str):
    selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    entries = FoodEntry.objects.filter(user=request.user, date=selected_date)

    # Aggregate macronutrient totals
    total_protein = sum(entry.protein or 0 for entry in entries)
    total_carbs = sum(entry.carbs or 0 for entry in entries)
    total_fats = sum(entry.fat or 0 for entry in entries)

    return render(request, 'tracker/daily_activity.html', {
        'entries': entries,
        'selected_date': selected_date,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fats': total_fats,
    })
def calendar_view(request):
    return render(request, 'tracker/calendar_view.html')