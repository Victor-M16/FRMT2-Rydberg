from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    NewUser, 
    Revenue, 
    Transaction, 
    Collection_instance,
    Business,
    Property,
    )
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin


def landing(request):
    context = {
        'users':NewUser.objects.all(),
        'collection_instances':Collection_instance.objects.all(),
        'transactions':Transaction.objects.all(),
        'revenue_types':Revenue.objects.all(),
    }
    #return render(request, 'users/dashboards/base.html', context )
    return render(request, 'users/landing.html', context )

@login_required
def home(request):
    context = {
        'users':NewUser.objects.all(),
        'collection_instances':Collection_instance.objects.all(),
        'transactions':Transaction.objects.all(),
        'revenue_types':Revenue.objects.all(),
    }
    return render(request, 'users/home.html', context )

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
    """
    current_user = request.user  # Get the currently logged-in user


     if current_user.user_type == "Revenue Creator":
        return render(request, 'users/dashboards/revenueCreator.html')
    elif current_user.user_type == "Collector":
        return render(request, 'users/dashboards/collector.html')
    else:
        return render(request, 'users/dashboards/councilOfficial.html')   
    """   
    context = {
        'users':NewUser.objects.all(),
        'collection_instances':Collection_instance.objects.all(),
        'transactions':Transaction.objects.all(),
        'revenue_types':Revenue.objects.all(),
    }
    return render(request, 'users/home.html', context )


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
def displayCollectors(request):


    context = {
        'users': NewUser.objects.all(),
        
    }

    return render(request, 'users/councilOfficial/collectors.html', context)


@login_required
def displayProperties(request):


    context = {
        'users': NewUser.objects.all(),
        
    }

    return render(request, 'users/properties/properties.html', context)

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




#####################################################################################################
class Collection_instanceListView(LoginRequiredMixin, ListView):
    model = Collection_instance
    template_name = "users/councilOfficial/collection_instances.html"
    context_object_name = "collection_instances"


class Collection_instanceDetailView(LoginRequiredMixin, DetailView):
    model = Collection_instance


class Collection_instanceCreateView(LoginRequiredMixin, CreateView):
    model = Collection_instance 
    fields = ['name','jurisdiction','collector','collected_revenue', 'amount']

    #def form_valid(self, form):
     #   form.instance.author = self.request.user
      #  return super().form_valid(form)


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








#####################################################################################################

class NewUserListView(LoginRequiredMixin, ListView):
    model = NewUser
    template_name = "users/admin/users.html"
    context_object_name = 'users'

class NewUserDetailView(LoginRequiredMixin, DetailView):
    model = NewUser
    template_name = "users/profiles/newuser_detail.html"

class NewUserUpdateView(LoginRequiredMixin, UpdateView):
    model = NewUser 
    form_class = CustomUserChangeForm

    def form_valid(self, form):
        form.instance.email = self.request.user.email
        form.instance.user_name = self.request.user.user_name
        form.instance.user_type = self.request.user.user_type

        return super().form_valid(form)

class NewUserCreateView(LoginRequiredMixin, CreateView):
    model = NewUser 
    form_class = CustomUserCreationForm










#####################################################################################################
class BusinessListView(LoginRequiredMixin, ListView):
    model = Business
    template_name = "users/businesses/business_list.html"
    context_object_name = "businesses"


class BusinessDetailView(LoginRequiredMixin, DetailView):
    model = Business
    template_name = "users/businesses/business_detail.html"


class BusinessCreateView(LoginRequiredMixin, CreateView):
    model = Business 
    fields = ['name','owner','description',]
    template_name = "users/businesses/business_form.html"

    #def form_valid(self, form):
     #   form.instance.author = self.request.user
      #  return super().form_valid(form)


class BusinessUpdateView(LoginRequiredMixin, UpdateView):
    model = Business 
    fields = ['name','owner','description',]
    template_name = "users/businesses/business_form.html"

    #def form_valid(self, form):
    #    form.instance.author = self.request.user
    #    return super().form_valid(form)   

class BusinessDeleteView(LoginRequiredMixin, DeleteView):
    model = Business 
    success_url = '/businesses/'
    template_name = "users/businesses/business_confirm_delete.html"
    






#####################################################################################################
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "users/transactions/transaction_list.html"
    context_object_name = "transactions"


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "users/transactions/transaction_detail.html"


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction 
    fields = ['name','owner','description',]
    template_name = "users/transactions/transaction_form.html"

    #def form_valid(self, form):
     #   form.instance.author = self.request.user
      #  return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction 
    fields = ['name','owner','description',]
    template_name = "users/transactions/transaction_form.html"

    #def form_valid(self, form):
    #    form.instance.author = self.request.user
    #    return super().form_valid(form)   

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction 
    success_url = '/transactions/'
    template_name = "users/transactions/transaction_confirm_delete.html"





#####################################################################################################
class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = "users/properties/properties.html"
    context_object_name = "properties"


class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = "users/properties/property_detail.html"


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property 
    fields = ['name','plot_number','capital_value','land_use','rates_owed',]
    template_name = "users/properties/property_form.html"

    #def form_valid(self, form):
     #   form.instance.author = self.request.user
      #  return super().form_valid(form)


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property 
    fields = ['name','plot_number','capital_value','land_use','rates_owed',]
    template_name = "users/properties/property_form.html"

    #def form_valid(self, form):
    #    form.instance.author = self.request.user
    #    return super().form_valid(form)   

class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property 
    success_url = '/properties/'
    template_name = "users/properties/property_confirm_delete.html"