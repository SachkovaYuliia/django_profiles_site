from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm
from django.contrib.auth import authenticate

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'location', 'avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            max_size = 2 * 1024 * 1024  
            if avatar.size > max_size:
                raise ValidationError("The image file is too large. Maximum size is 2MB.")
        return avatar

class PasswordChangeForm(BasePasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password): 
            raise ValidationError("Current password is incorrect.")
        return old_password

    def clean_new_password_confirm(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise ValidationError("New passwords do not match.")
        if new_password == self.cleaned_data.get('old_password'):
            raise ValidationError("New password cannot be the same as the old password.")
        return new_password_confirm