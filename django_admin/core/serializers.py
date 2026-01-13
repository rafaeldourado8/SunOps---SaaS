from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(default=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'is_active']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
