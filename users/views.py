from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import NewUser, Council, Service, Notification, Transaction, Issue, Business


def home(request):
    return render(request, 'users/home.html' )

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


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def dashboard(request):
    current_user = request.user  # Get the currently logged-in user
        
    if current_user.user_type == "Business Owner":
        return render(request, 'users/dashboards/businessOwner.html')
    elif current_user.user_type == "Land Owner":
        return render(request, 'users/dashboards/landOwner.html')
    elif current_user.user_type == "Collector":
        return render(request, 'users/dashboards/collector.html')
    else:
        return render(request, 'users/dashboards/councilOfficial.html')

@login_required
def parameters(request):
    return render(request, 'users/councilOfficial/parameters.html')

"""
@login_required
def displayBusinesses(request, councilID):
    businesses = Business.objects.filter(councilID=selected_council)
    return render(request, 'business_list.html', {'businesses': businesses})
"""