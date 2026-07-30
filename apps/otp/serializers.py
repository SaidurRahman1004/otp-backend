from rest_framework import serializers
from .models import OTPMessage

class OTPMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPMessage
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
