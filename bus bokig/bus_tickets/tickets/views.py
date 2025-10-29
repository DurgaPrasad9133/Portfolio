from time import sleep

from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.core.cache import cache


# Create your views here.
class Passengers(APIView):

    def get(self,request):
        query = CustomUser.objects.filter(Q(is_active=True) & Q(role='P'))
        serialized_query=CustomUserSerializer(query,many=True)
        return Response(serialized_query.data)
    def post(self,request):
        serialized = CustomUserSerializer(data=request.data)
        try:
            if serialized.is_valid():
                serialized.save()
                return Response("Success")
            else:
                return Response(serialized.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class Busses(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        query = Buses.objects.all()
        serialized_query=BusesSerializer(query,many=True)
        sleep(0.3)
        return Response(serialized_query.data)
    def post(self,request):
        serialized = BusesSerializer(data=request.data)
        try:
            if serialized.is_valid():
                serialized.save()
                return Response("Success")
            else:
                print(serialized.errors)
                return Response(serialized.errors, status=400)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=500)


class BusSearch(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        starts_from = request.GET.get('starts_from')
        going_to = request.GET.get('going_to')
        running_day = request.GET.get('running_day')
        filters = {}
        if starts_from:
            filters['starts_from__iexact'] = starts_from
        if going_to:
            filters['going_to__iexact'] = going_to
        if running_day:
            filters['running_day__iexact'] = running_day
        buses = Buses.objects.filter(**filters)
        serialized = BusesSerializer(buses, many=True)
        return Response(serialized.data)


class SeatAvailability(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        bus_id = request.GET.get('bus_id')
        trip_date = request.GET.get('trip_date')
        try:
            bus = Buses.objects.get(id=bus_id)
            booked_seats = Bookings.objects.filter(booked_Bus=bus, trip_date=trip_date, status='C').values_list('seat_no', flat=True)
            booked_seats_flat = [seat for sublist in booked_seats for seat in sublist]
            available_lower = [seat for seat in bus.lower_seats if seat not in booked_seats_flat]
            available_upper = [seat for seat in bus.upper_seats if seat not in booked_seats_flat]
            return Response({
                'available_lower_seats': available_lower,
                'available_upper_seats': available_upper
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class Bookings(APIView):

    def get(self,request):
        query = Bookings.objects.all()
        serialized_query=BookingsSerializer(query,many=True)
        return Response(serialized_query.data)
    def post(self,request):
        seat_no = request.data.get('seat_no', [])
        bus_id = request.data.get('booked_Bus')
        trip_date = request.data.get('trip_date')
        seat_position = request.data.get('seat_position')
        bus = Buses.objects.get(id=bus_id)
        booked_seats = Bookings.objects.filter(booked_Bus=bus, trip_date=trip_date, status='C').values_list('seat_no', flat=True)
        booked_seats_flat = [seat for sublist in booked_seats for seat in sublist]
        for seat in seat_no:
            if seat in booked_seats_flat:
                return Response({'error': f'Seat {seat} is already booked.'}, status=400)
        serialized = BookingsSerializer(data=request.data)
        try:
            if serialized.is_valid():
                serialized.save()
                return Response('Success')
            else:
                return Response(serialized.errors, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully"}, status=201)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user_id = request.data.get('username')
            access = response.data.get('access')
            refresh = response.data.get('refresh')
            if access:
                cache.set(f'access:{user_id}', access, timeout=300)  # 5 min
            if refresh:
                cache.set(f'refresh:{user_id}', refresh, timeout=600)  # 10 min
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # You may want to update the refresh token in Redis as well
            refresh = request.data.get('refresh')
            access = response.data.get('access')
            if refresh and access:
                # Find user by refresh token if needed, or store by token value
                cache.set(f'access_from_refresh:{refresh}', access, timeout=300)
        return response
