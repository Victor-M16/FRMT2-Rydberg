from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import NewUser, Revenue, Transaction, Collection_instance
from django.views.generic import ListView

def home(request):
    context = {
        'users':NewUser.objects.all(),
        'collection_instances':Collection_instance.objects.all(),
        'transactions':Transaction.objects.all(),
        'revenue_types':Revenue.objects.all(),
    }
    return render(request, 'users/home.html', context )


class Collection_instanceListView(ListView):
    model = Collection_instance
    template_name = 'users/home.html'
    content_object_name = 'collection_instances'

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
    current_user = request.user  # Get the currently logged-in user
        
    if current_user.user_type == "Revenue Creator":
        return render(request, 'users/profiles/revenueCreator.html')
    elif current_user.user_type == "Collector":
        return render(request, 'users/profiles/collector.html')
    elif current_user.user_type == "council official":
        return render(request, 'users/profiles/councilOfficial.html')
    else:
        return render(request, 'users/profiles/base.html')
    



@login_required
def dashboard(request):
    current_user = request.user  # Get the currently logged-in user
        
    if current_user.user_type == "Revenue Creator":
        return render(request, 'users/dashboards/revenueCreator.html')
    elif current_user.user_type == "Collector":
        return render(request, 'users/dashboards/collector.html')
    else:
        return render(request, 'users/dashboards/councilOfficial.html')

@login_required
def parameters(request):
    current_user = request.user  # Get the currently logged-in user
        
    if current_user.user_type == "Revenue Creator":
        return render(request, 'users/revenueCreator/parameters.html')
    else:
       return render(request, 'users/councilOfficial/parameters.html')


@login_required
def displayUsers(request):
    context = {
        'users': NewUser.objects.all()
    }
    return render(request, 'users/admin/users.html', context)