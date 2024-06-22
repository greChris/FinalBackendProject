from django.shortcuts import render
from django.http import HttpResponse
import json
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView,DestroyAPIView
from rest_framework import generics,viewsets
from .serializers import MenuSerializer,BookingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Menutable,BookingTable
from .forms import BookForm
from rest_framework import serializers
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def about(request):
    return render(request, "about.html")
def index(request):
    return render(request,'index.html',{})
def menu(request):
    menu_items = Menutable.objects.all()
    return render(request, 'menu.html', {"menu": menu_items})
def book(request):
    form = BookForm
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)

def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    print("date: ", date)
    bookings = BookingTable.objects.all().filter(BookingDate = date)
    booking_json = serializers.Serializer('json', bookings)
    return render(request, 'bookings.html', {'bookings': booking_json})
@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = BookingTable.objects.filter(BookingDate=data['booking_date']).filter(
            no_of_guests=data['no_of_guests']).exists()
        if exist==False:
            booking = BookingTable(
                name=data['name'],
                booking_date=data['booking_date'],
                no_of_guests=data['no_of_guests'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = BookingTable.objects.all().filter(BookingDate=date)
    booking_json = serializers.Serializer('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')


class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Menutable.objects.all()
    serializer_class = MenuSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.RetrieveDestroyAPIView):

    queryset = Menutable.objects.all()
    serializer_class = MenuSerializer

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BookingTable.objects.all()
    serializer_class = BookingSerializer