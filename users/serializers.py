# serializers.py
from rest_framework import serializers
from .models import NewUser
from .models import Business
from .models import Property, Transaction, Collection_instance,CollectionInstance,CollectionType, Location


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id', 'email', 'user_name', 'user_type')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class CollectionTypeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CollectionType
        fields = '__all__'

class CollectionInstanceSerializer(serializers.ModelSerializer):
    collection_type = CollectionTypeSerializer()
    location = LocationSerializer()
    # location_id = serializers.PrimaryKeyRelatedField(source='location', read_only=True)

    class Meta:
        model = CollectionInstance
        # fields = ['location', 'location_id', 'collection_type', 'amount']
        fields ="__all__"



class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'plot_number', 'land_use', 'capital_value', 'name', 'rates_owed']



class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'name']


class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = ['id', 'date', 'collection_instance_id', 'amount', 'description', 'transaction_type']
