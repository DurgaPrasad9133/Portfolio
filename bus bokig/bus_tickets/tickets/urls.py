from django.urls import path
from .views import *

urlpatterns = [
    path('passengers/', Passengers.as_view(), name='passengers'),
    path('buses/', Busses.as_view(), name='buses'),
    path('bookings/', Bookings.as_view(), name='bookings'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('buses/search/', BusSearch.as_view(), name='search_buses'),
    path('buses/seat-availability/', SeatAvailability.as_view(), name='seat_availability'),

]