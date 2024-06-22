from rest_framework.serializers import ModelSerializer
from .models import Menutable,BookingTable

class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menutable
        fields = '__all__'

class BookingSerializer(ModelSerializer):
    class Meta:
        model = BookingTable
        fields = '__all__'