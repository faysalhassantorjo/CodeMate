from .models import UserProfile
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')
#     last_activity = models.DateTimeField(default=timezone.now)
#     is_online = models.BooleanField(default=False)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
