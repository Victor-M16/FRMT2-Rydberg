# serializers.py
from rest_framework import serializers
from .models import NewUser
from .models import Business
from .models import Property, Transaction, Collection_instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id', 'email', 'user_name', 'user_type')


class CollectionInstanceSerializer(serializers.ModelSerializer):
    location_id = serializers.PrimaryKeyRelatedField(source='location', read_only=True)

    class Meta:
        model = Collection_instance
        fields = ['location', 'location_id', 'type_to_collect', 'amount']


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
