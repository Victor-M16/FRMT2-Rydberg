from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NewUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ['email', 'user_name', 'user_type', 'password1', 'password2']

    user_type = forms.ChoiceField(
        label='User Type',
        widget=forms.Select,
        choices= NewUser.USER_TYPE_CHOICES, 
        required=True,
    )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = NewUser
        fields = ['email', 'user_name', 'user_type']

    user_type = forms.ChoiceField(
        label='User Type',
        widget=forms.Select,
        choices=NewUser.USER_TYPE_CHOICES,  
        required=True,
    )


