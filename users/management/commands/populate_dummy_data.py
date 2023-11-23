# your_app/management/commands/populate_dummy_data.py
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from users.models import Collection_instance, Location, NewUser, Property, CollectionType, CollectionInstance
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import random
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        self.populate_locations()
        self.populate_users()
        self.populate_collection_types()
        self.populate_dummy_assignments()
        self.populate_dummy_properties() 

    def populate_locations(self):
        locations = ['Limbe', 'Chileka', 'Ndirande', 'Chirimba', 'Mbayani', 'Mandala', 'Lunzu', 'Kanjedza', 'Chinyonga', 'Bangwe']

        for loc in locations:
            Location.objects.create(name=loc)
            pass


    def populate_dummy_assignments(self):
        # Your logic to create dummy CollectionInstance instances
        locations = Location.objects.all()
        collectors = NewUser.objects.filter(user_type='Collector')
        collection_types = CollectionType.objects.all()

        for _ in range(10):  # You can adjust the number of instances you want to create
            # Choose random values for the fields
            location = random.choice(locations)
            collector = random.choice(collectors)
            collection_type = random.choice(collection_types)
            amount = random.uniform(100, 1000)  # Generate a random amount between 100 and 1000

            # Generate a random date within the last year
            random_days_ago = random.randint(1, 365)
            date_time = timezone.now() - timedelta(days=random_days_ago)

            # Create CollectionInstance instance
            CollectionInstance.objects.create(
                location=location,
                collector=collector,
                collection_type=collection_type,
                amount=amount,
                date_time=date_time
            )

        pass



   
    def populate_collection_types(self):
        
        collection_types = ['Market Fee', 'City Rate', 'License Fee', 'Parking Fee', 'Business Tax']

        # Dummy data for locations
        locations = Location.objects.all()

        for location_name in locations:
            # Check if the location already exists; create it if not
            try:
                location = Location.objects.get(name=location_name)
            except ObjectDoesNotExist:
                location = Location.objects.create(name=location_name)

            # Create CollectionType instances with the given location
            amount = random.randint(200,100000)
            for collection_type_name in collection_types:
                CollectionType.objects.create(name=collection_type_name, location=location, amount=amount)

    def populate_dummy_properties(self):
        # Your logic to create dummy Property instances
        locations = Location.objects.all()
        properties = ['Ngulube Residence','Twaha Residence', 'Banda Residence','Rydberg Starck', 'MUBAS', 'Golden Peacock', 'National Bank Chichiri Service Centre', 'Chichiri Shopping Mall', 'Mall of Africa','ESCOM Chichiri Power Station']
        
        for name in properties:  # You can adjust the number of instances you want to create
            # Choose random values for the fields
            plot_number = f'P-{random.randint(1000, 9999)}'  # Generating a random plot number

            # Use the name of the property to determine land use
            if name in ['Ngulube Residence', 'Twaha Residence', 'Banda Residence']:  # Corrected conditional check
                land_use = 'Residential'
            else:
                land_use = 'Commercial'

            capital_value = random.uniform(100000, 1000000)  # Generate a random capital value between 100,000 and 1,000,000
            name = random.choice(properties)  # Generating a random name
            location = random.choice(locations)

            # Calculate rates_owed based on land_use
            if land_use == 'Commercial':
                rate_multiplier = 0.0020
            else:
                rate_multiplier = 0.0013

            rates_owed = capital_value * rate_multiplier

            # Create Property instance
            Property.objects.create(
                plot_number=plot_number,
                land_use=land_use,
                capital_value=capital_value,
                name=name,
                rates_owed=rates_owed,
                location=location
            )

        pass
    
    
    def populate_users(self):
        emails = ['victor@rsl.com', 'fahad@rsl.com', 'grace@rsl.com', 'tionge@rsl.com', 'jayne@rsl.com', 'cuthbert@rsl.com']
        users = ['Victor Mjimapemba', 'Fahad Twaha', 'Grace Chiwaya', 'Tionge Ngulube','Jayne Banda', 'Cuthbert Magawa']
        user_types = ['Admin', 'Collector', 'Council Official', 'Revenue Creator', 'Collector', 'Collector', ]
        passwords = ['rsl#admin', 'rsl#collect', 'rsl#official', 'rsl#create', 'rsl#collect', 'rsl#collect',]  # Choose your passwords

        for email, user_name, user_type, password in zip(emails, users, user_types, passwords):
            is_staff = True if user_type == 'Admin' else False

            # Create a NewUser instance
            new_user = NewUser.objects.create(email=email, user_name=user_name, user_type=user_type, is_staff=is_staff)

            # Set the password using set_password
            new_user.set_password(password)

            # Save the user instance to persist changes to the database
            new_user.save()
