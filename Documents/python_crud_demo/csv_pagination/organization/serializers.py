from rest_framework import serializers
from .models import User,Meter
from django.contrib.auth.hashers import make_password
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = User.objects.create(**validated_data)
        return user       


class Meterserializer(serializers.ModelSerializer):
    class Meta:
        model = Meter      
        fields = ('serial_number','inc_name','proprietor_name','meter_measurement','diff_units','avg_unit','power_utility_index','power_station_name','usage_type','csi_index')        