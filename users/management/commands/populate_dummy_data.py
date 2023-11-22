# your_app/management/commands/populate_dummy_data.py
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from users.models import Collection_instance, Location, NewUser, Revenue

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        self.populate_locations()
        self.populate_users()
        self.populate_revenue_types()
        self.populate_dummy_assignments()

    def populate_locations(self):
        locations = ['Limbe', 'Chileka', 'Ndirande', 'Chirimba', 'Mbayani', 'Mandala', 'Lunzu', 'Chileka', 'Chinyonga', 'Bangwe']

        for loc in locations:
            Location.objects.create(name=loc)
            pass

    def populate_users(self):
        # Your logic to create dummy NewUser instances
        pass

    def populate_revenue_types(self):
        # Your logic to create dummy Revenue instances
        pass

    def populate_dummy_assignments(self):
        # Your logic to create dummy Collection_instance instances
        pass
