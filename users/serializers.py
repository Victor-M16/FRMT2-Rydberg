# serializers.py
from rest_framework import serializers
from .models import NewUser
from .models import Business

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id', 'email', 'user_name', 'user_type')



class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'name']
