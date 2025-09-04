from django.shortcuts import render, redirect
from .forms import UserProfileForm, CustomRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .models import UserProfile
from .utils import calculate_macro_goals
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404

from django.contrib import messages
import random
from django.db import transaction

@login_required
def profile_setup(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.macro_goal_calories = calculate_macro_goals(profile)
            profile.save()
            return redirect('dashboard')  # or 'home'
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'accounts/profile_setup.html', {'form': form})

@login_required
def profile_view(request):
    try:
        # Use OneToOne relation to access UserProfile
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Auto-create a blank profile if it doesn't exist
        profile = UserProfile.objects.create(
            user=request.user,
            age=0,
            weight=0.0,
            height=0.0,
            activity_level='',
            goal=''
        )

    return render(request, 'accounts/profile.html', {'profile': profile})
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        if not request.POST.get('remember_me'):
            request.session.set_expiry(0)
        return redirect('dashboard')

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = CustomRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            user = form.save()
            # Safely create UserProfile if it doesn't exist
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'age': 0,
                    'weight': 0.0,
                    'height': 0.0,
                    'activity_level': '',
                    'goal': ''
                }
            )
            login(request, user)
        return redirect('profile_setup')

    return render(request, 'accounts/register.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            # Generate a new temporary password
            new_password = f'newpass{random.randint(1000,9999)}'
            user.password = make_password(new_password)
            user.save()
            messages.success(request, f'New password is: {new_password}')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        return redirect('login')  # or redirect to same page
    return render(request, 'accounts/forgot_password.html')

def logout_view(request):
    logout(request)
    return redirect('login')
