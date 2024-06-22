from django.forms import ModelForm
from .models import BookingTable

class BookForm(ModelForm):
    class Meta:
        model = BookingTable
        fields = '__all__'
