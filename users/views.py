from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, LocationForm, CollectionTypeForm, CollectionInstanceForm
from .models import NewUser, Revenue, Transaction, Collection_instance
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CollectionType, CollectionInstance

def home(request):
    context = {
        'users':NewUser.objects.all(),
        'collection_instances':Collection_instance.objects.all(),
        'transactions':Transaction.objects.all(),
        'revenue_types':Revenue.objects.all(),
    }
    return render(request, 'users/home.html', context )

def index(request):
    return render(request, 'newTemplates/index.html', {} )

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
    collection_type = CollectionType.objects.all()
    collection_instance = CollectionInstance.objects.all()
    return render(request, 'newTemplates/collections.html', {
        'collectionType': collection_type, 'collectionInstance': collection_instance})

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

def addLocation(request):
    submitted = False
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/collections/location/add?submitted=True')
    else:
        form = LocationForm
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'newTemplates/add_location.html', {'form':form, 'submitted':submitted})

def addCollectionType(request):
    submitted = False
    if request.method == "POST":
        form = CollectionTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/collections/type/add?submitted=True')
    else:
        form = CollectionTypeForm
        if 'submitted' in request.GET:
            submitted = True
        
    form = CollectionTypeForm
    return render(request, 'newTemplates/add_collection_type.html', {'form':form, 'submitted':submitted})

# def editCollectionType(request, typeID):
#     collectionType = CollectionType.objects.get(pk=typeID)
#     return render(request, 'newTemplates/edit_collection_types.html', {'collectionType':collectionType})

def deleteCollectionType(request, collectionType_id):
    collectionType = CollectionType.objects.get(pk=collectionType_id)
    # collectionType = get_object_or_404(CollectionType, id=collectionType_id)
    collectionType.delete()
    return redirect('collections')

# class CollectionTypeDeleteView(DeleteView):
#     model = CollectionType
#     success_url = '/collections/'

def addCollectionInstance(request):
    submitted = False
    if request.method == "POST":
        form = CollectionInstanceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/collections/instance/add?submitted=True')
    else:
        form = CollectionInstanceForm
        if 'submitted' in request.GET:
            submitted = True
        
    form = CollectionInstanceForm
    return render(request, 'newTemplates/add_collection_instance.html', {'form':form, 'submitted':submitted})

def deleteCollectionInstance(request, collectionInstance_id):
    collectionInstance = CollectionInstance.objects.get(pk=collectionInstance_id)
    # collectionType = get_object_or_404(CollectionType, id=collectionType_id)
    collectionInstance.delete()
    return redirect('collections')