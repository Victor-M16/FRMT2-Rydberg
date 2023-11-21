# serializers.py
from rest_framework import serializers
from .models import NewUser

class NewUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewUser
        fields = ['user_name', 'email', 'is_staff']  # Add your custom fields as needed
