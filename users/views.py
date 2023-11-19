from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import NewUser, Revenue, Transaction, Collection_instance
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    context = {
        'users':NewUser.objects.all(),
        'collection_instances':Collection_instance.objects.all(),
        'transactions':Transaction.objects.all(),
        'revenue_types':Revenue.objects.all(),
    }
    return render(request, 'users/home.html', context )

class Collection_instanceListView(LoginRequiredMixin, ListView):
    model = Collection_instance
    template_name = "users/councilOfficial/collection_instances.html"
    context_object_name = "collection_instances"


class Collection_instanceDetailView(LoginRequiredMixin, DetailView):
    model = Collection_instance


class Collection_instanceCreateView(LoginRequiredMixin, CreateView):
    model = Collection_instance 
    fields = ['name','jurisdiction','collector','collected_revenue', 'amount']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class Collection_instanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Collection_instance 
    fields = ['name','jurisdiction','collector','collected_revenue', 'amount']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   

class Collection_instanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Collection_instance 
    success_url = '/CI/'
    

class my_Collection_instanceListView(LoginRequiredMixin, ListView):
    model = Collection_instance
    template_name = "users/collector/collection_instances.html"
    context_object_name = "my_collection_instances"

    def get_queryset(self):
        # Assuming current_user is the user making the request
        current_user = self.request.user

        # Filter the Collection_instance queryset based on the current user
        queryset = Collection_instance.objects.filter(collector=current_user)

        return queryset

@login_required
def displayCollectionInstances(request):
    
    current_user = request.user  # Get the currently logged-in user
    
    
    context = {
        'collection_instances': Collection_instance.objects.all(),
        'my_collection_instances' : Collection_instance.objects.filter(collector=current_user)
    }

    if current_user.user_type == "Council Official":
        return render(request, 'users/councilOfficial/collection_instances.html', context)
    else:
        return render(request, 'users/collector/collection_instances.html', context)
    

def faq(request):
    return render(request, 'users/faq.html')  


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
    elif current_user.user_type == "Council Official":
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
        'users': NewUser.objects.all(),
        
    }

    return render(request, 'users/admin/users.html', context)

@login_required
def displayProperties(request):


    context = {
        'users': NewUser.objects.all(),
        
    }

    return render(request, 'users/properties.html', context)

#New added pages
def properties(request):
    return render(request, 'newTemplates/properties.html', {})

def users(request):
    return render(request, 'newTemplates/users.html', {})

def market(request):
    return render(request, 'newTemplates/market.html', {})

def collections(request):
    return render(request, 'newTemplates/collections.html', {})

def usersProfile(request):
    return render(request, 'newTemplates/users-profile.html', {})

def collectorsProfile(request):
    return render(request, 'newTemplates/collectors-profile.html', {})

def collectorDashboard(request):
    return render(request, 'newTemplates/collector-dash.html', {})

def collectorInstances(request):
    return render(request, 'newTemplates/collector-Instances.html', {})

def collectorDashProfile(request):
    return render(request, 'newTemplates/collector-dash-profile.html', {})