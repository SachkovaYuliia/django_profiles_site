from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import RegistrationForm, UserProfileForm, PasswordChangeForm
from django.contrib import messages

def home(request):
    return render(request, 'accounts/base.html')

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, "Ваш обліковий запис успішно створено!")
            return redirect('login')  
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    user_profile = request.user.profile
    all_profiles = UserProfile.objects.all()

    return render(request, 'accounts/profile.html', {
        'user_profile': user_profile,
        'all_profiles': all_profiles,
    })

@login_required
def edit_profile_view(request):
    user_profile = request.user.profile  
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль успішно оновлено!")
            return redirect('profile')  
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  
            messages.success(request, 'Ваш пароль успішно змінено!')
            return redirect('profile')  
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
