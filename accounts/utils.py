def calculate_macro_goals(profile):
    # Mifflin-St Jeor Equation
    bmr = 10 * profile.weight + 6.25 * profile.height - 5 * profile.age
    if profile.user.userprofile.gender == 'male':  # Add gender field if needed
        bmr += 5
    else:
        bmr -= 161

    activity_factors = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'extra': 1.9,
    }

    calories = bmr * activity_factors.get(profile.activity_level, 1.2)

    if profile.goal == 'cut':
        calories -= 300
    elif profile.goal == 'bulk':
        calories += 300

    return int(calories)
