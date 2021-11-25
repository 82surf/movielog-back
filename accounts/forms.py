from django import forms
from django.contrib.auth import get_user_model
from django.forms import fields


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'name', 'profile_image', 'is_private')