from django.contrib import admin
from .models import CustomUser, Buses, Bookings

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'age', 'gender', 'role', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('gender', 'role', 'is_active')

class BusesAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_no', 'bus_type', 'starts_from', 'going_to', 'running_day', 'is_active')
    search_fields = ('name', 'service_no', 'starts_from', 'going_to')
    list_filter = ('bus_type', 'running_day', 'is_active')

class BookingsAdmin(admin.ModelAdmin):
    list_display = ('booked_by', 'booked_Bus', 'status', 'seat_no', 'seat_position', 'trip_date', 'booked_time')
    search_fields = ('booked_by__username', 'booked_Bus__name', 'seat_no')
    list_filter = ('status', 'seat_position', 'trip_date')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Buses, BusesAdmin)
admin.site.register(Bookings, BookingsAdmin)
