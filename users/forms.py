from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NewUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ['email', 'user_name', 'user_type', 'is_staff', 'is_superuser', 'password1', 'password2']

    user_type = forms.ChoiceField(
        label='User Type',
        widget=forms.Select,
        choices=NewUser.USER_TYPE_CHOICES,
        required=True,
    )

    is_staff = forms.BooleanField(
        label='Create as Staff',
        required=False,
    )

    is_superuser = forms.BooleanField(
        label='Create as Superuser',
        required=False,
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']

        # Check if the user is to be created as staff
        user.is_staff = self.cleaned_data.get('is_staff')

        # Check if the user is to be created as a superuser
        if self.cleaned_data.get('is_superuser'):
            user.is_staff = True
            user.is_superuser = True

        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = NewUser
        fields = ['email', 'user_name', 'user_type', 'is_staff', 'is_superuser']

    user_type = forms.ChoiceField(
        label='User Type',
        widget=forms.Select,
        choices=NewUser.USER_TYPE_CHOICES,  
        required=True,
    )

    is_staff = forms.BooleanField(
        label='Is Staff',
        required=False,
    )

    is_superuser = forms.BooleanField(
        label='Is Superuser',
        required=False,
    )


