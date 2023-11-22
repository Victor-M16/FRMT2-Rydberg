from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from django.db import models
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
    Location,
    )
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

#API views##############################################
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from .serializers import BusinessSerializer, PropertySerializer, TransactionSerializer, CollectionInstanceSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({'status': True, 'user': serializer.data, 'token': token.key})
        else:
            return Response({'status': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




class BusinessByLocationView(ListAPIView):
    serializer_class = BusinessSerializer

    def get_queryset(self):
        location_id = self.kwargs['location_id']
        return Business.objects.filter(location_id=location_id)


@api_view(['GET'])
def get_user_active_assignment(request, user_id):
    try:
        # Assuming you have a way to determine the current assignment for the user
        user_assignment = Collection_instance.objects.filter(collector_id=user_id, date_time__lte=timezone.now()).latest('date_time')
        serializer = CollectionInstanceSerializer(user_assignment)
        return Response(serializer.data)
    except Collection_instance.DoesNotExist:
        return Response({'error': 'No active assignment for the user'}, status=404)
 
class PropertiesByLocationView(APIView):

    def get(self, request, location_id):
        properties = Property.objects.filter(location_id=location_id)
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)



class TransactionCreateView(APIView):

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)



#actual FRMT functionality views######################
class Home(LoginRequiredMixin, View):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):

        
        today = timezone.now().date()

        #day implementation
        total_amount_today = Collection_instance.objects.filter(date_time__date=today).aggregate(total_amount=Sum('amount'))['total_amount']

        #month implementation
        start_of_month = today.replace(day=1)

        total_amount_this_month = Collection_instance.objects.filter(
            date_time__date__gte=start_of_month,
            date_time__date__lte=today
        ).aggregate(total_amount=Sum('amount'))['total_amount']

        #year implementations
        start_of_year = today.replace(month=1, day=1)

        total_amount_this_year = Collection_instance.objects.filter(
            date_time__gte=start_of_year,
            date_time__lte=today
        ).aggregate(total_amount=Sum('amount'))['total_amount']


        # all-time implementations
        total_amount = Collection_instance.objects.all().aggregate(total_amount=Sum('amount'))['total_amount']

        # Get unique collection types and their counts
        collection_types_counts = (
            Collection_instance.objects.values('type_to_collect').annotate(count=models.Count('type_to_collect'))
        )

        collection_types = [item['type_to_collect'] for item in collection_types_counts]
        collection_types_values = [item['count'] for item in collection_types_counts]
        collection_types_counts_dict = {item['type_to_collect']: item['count'] for item in collection_types_counts}

        revenueTypes = []
        amounts = []

        queryset = Collection_instance.objects.all()

        for instance in queryset:
            revenueTypes.append(str(instance.type_to_collect))
            temp = str(instance.amount)
            amounts.append(temp)



        return {'revenueTypes':revenueTypes,
                'amounts':amounts,
                'collection_types':collection_types,
                'collection_types_values':collection_types_values,
                'total_amount': total_amount,
                'total_amount_this_year': total_amount_this_year,
                'total_amount_this_month': total_amount_this_month,
                'total_amount_today': total_amount_today,
                'users' : NewUser.objects.all(),
                'collection_instances':Collection_instance.objects.all(),
                'transactions':Transaction.objects.all(),
                'revenue_types':Revenue.objects.all(),
                }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)



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
    return render(request, 'users/councilOfficial/market.html', {})

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
    fields = ['location','collector','type_to_collect', 'amount']

    #def form_valid(self, form):
     #   form.instance.author = self.request.user
      #  return super().form_valid(form)


class Collection_instanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Collection_instance 
    fields = ['location','collector','type_to_collect', 'amount']

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


class TransactionAppCreateView(LoginRequiredMixin, CreateView):
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

    def get_queryset(self):
        return Property.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        locations_queryset = Location.objects.all()
        locations_list = []


        land_uses = Property.objects.values_list('land_use', flat=True).distinct()


        # Get unique land uses and their counts
        land_uses_counts = (
            Property.objects.values('land_use').annotate(count= models.Count('land_use'))
        )

        land_uses = [item['land_use'] for item in land_uses_counts]
        land_uses_values = [item['count'] for item in land_uses_counts]
        land_uses_counts_dict = {item['land_use']: item['count'] for item in land_uses_counts}



        for instance in locations_queryset:
            locations_list.append(str(instance.name))

        
        # Calculate property count
        property_count = self.get_queryset().count()

        # Get the highest valued property
        highest = self.get_queryset().order_by('-capital_value').first()

        # Calculate total rates due
        rates_due = self.get_queryset().aggregate(total_rates_due=Sum('rates_owed'))['total_rates_due']

        # Add additional context names and their corresponding values
        context['property_count'] = property_count
        context['highest_valued_property'] = highest
        context['total_rates_due'] = rates_due
        context['locations'] = locations_list
        context['land_uses'] = land_uses
        context['land_uses_values'] = land_uses_values

        return context


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