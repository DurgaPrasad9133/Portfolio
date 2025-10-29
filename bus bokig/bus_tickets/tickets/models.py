import datetime
from calendar import THURSDAY

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.utils import timezone
from django.db.models import DO_NOTHING


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    ROLES = [
        ('A','Admin'),
        ('P','Passenger')
    ]
    phone_number_validator=RegexValidator(r'^\d{10}$',"Phone number should be 10 digits")
    phone_number=models.IntegerField(validators=[phone_number_validator])
    age=models.IntegerField()
    address=models.CharField(max_length=150)
    gender=models.CharField(choices=GENDER_CHOICES,max_length=1)
    role=models.CharField(choices=ROLES , default='P',max_length=1)


class Buses(models.Model):
    BUS_TYPES = [
        ('AC', 'AC'),
        ('NON-AC', 'Non-AC'),
        ('SLEEPER', 'Sleeper'),
        ('SEMI-SLEEPER', 'Semi Sleeper'),
        ('LUXURY', 'Luxury'),
    ]
    DAYS_OF_WEEK = [
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    ]
    name=models.CharField(max_length=50)
    service_no=models.CharField(max_length=10)
    bus_type = models.CharField(max_length=20, choices=BUS_TYPES)
    starts_from=models.CharField(max_length=50)
    going_to=models.CharField(max_length=50)
    no_of_seats=models.IntegerField()
    lower_seats = models.JSONField(default=list, blank=True)
    upper_seats=models.JSONField(default=list, blank=True)
    lower_seat_price=models.IntegerField()
    upper_seat_price=models.IntegerField()
    running_day = models.CharField( max_length=12,  choices=DAYS_OF_WEEK,  default="MONDAY")
    is_active = models.BooleanField(default=True)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if (len(self.lower_seats)+len(self.upper_seats)) != self.no_of_seats:
            raise ValidationError({
                'seats': f"The number of seats ({len(self.lower_seats)+len(self.upper_seats)}) must match no_of_seats ({self.no_of_seats})."})


class Bookings(models.Model):
    BOOKING_STATUS = [
        ('C','Conformed'),
        ('F','Failed')
    ]
    SEAT_POSITION = [
        ('L','Lower'),
        ('U','Upper')
    ]
    booked_by=models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    booked_Bus=models.ForeignKey(Buses,on_delete=models.DO_NOTHING)
    booked_time=models.DateTimeField(default=timezone.now)
    status=models.CharField(choices=BOOKING_STATUS ,max_length=1)
    seat_no=models.JSONField(default=list, blank=True)
    seat_position=models.CharField(choices=SEAT_POSITION, max_length=1)
    is_deleted=models.IntegerField(default=0)
    trip_date=models.DateTimeField(default=timezone.now)
