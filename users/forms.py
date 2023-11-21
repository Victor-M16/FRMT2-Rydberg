from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NewUser, Location, CollectionType, CollectionInstance

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
    
class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('name',)
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'})
        }

class CollectionTypeForm(ModelForm):
    class Meta:
        model = CollectionType
        fields = ('name', 'location', 'amount')
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.Select(attrs={'class':'form-select'}),
            'amount': forms.TextInput(attrs={'class':'form-control'}),
        }
        

class CollectionInstanceForm(ModelForm):
    class Meta:
        model = CollectionInstance
        fields = ('location', 'collector', 'collection_type', 'amount')
        
        widgets = {
            'location': forms.Select(attrs={'class':'form-select'}),
            'collector': forms.Select(attrs={'class':'form-select'}),
            'collection_type': forms.Select(attrs={'class':'form-select'}),
            'amount': forms.TextInput(attrs={'class':'form-control'}),
        }

