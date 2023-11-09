from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm


def home(request):
    return render(request, 'users/home.html' )

def index(request):
    return render(request, 'users/index2.html')

@login_required
def profile(request):
    return render(request, 'users/profile.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            Username = form.cleaned_data.get('user_name')
            messages.success(request, f'An account for {Username} has been created. You may now log in.')
            return redirect('frmt-login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})