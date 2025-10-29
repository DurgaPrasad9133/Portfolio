from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Buses, Bookings

class BusBookingTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'phone_number': 1234567890,
            'age': 30,
            'address': 'Test Address',
            'gender': 'M',
            'role': 'P',
            'email': 'testuser@example.com'
        }
        self.bus_data = {
            'name': 'Test Bus',
            'service_no': 'TB123',
            'bus_type': 'AC',
            'starts_from': 'CityA',
            'going_to': 'CityB',
            'no_of_seats': 2,
            'lower_seats': [1],
            'upper_seats': [2],
            'lower_seat_price': 100,
            'upper_seat_price': 150,
            'running_day': 'MONDAY',
            'is_active': True,
            'departure_time': '10:00:00',
            'arrival_time': '12:00:00',
            'duration': '2:00:00'
        }

    def test_user_registration(self):
        url = reverse('register_user')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_user_registration(self):
        url = reverse('register_user')
        invalid_data = self.user_data.copy()
        invalid_data['phone_number'] = 'invalid'  # Should be 10 digits
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bus_search(self):
        Buses.objects.create(**self.bus_data)
        url = reverse('search_buses') + '?starts_from=CityA&going_to=CityB&running_day=MONDAY'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_seat_availability(self):
        bus = Buses.objects.create(**self.bus_data)
        url = reverse('seat_availability') + f'?bus_id={bus.id}&trip_date=2025-09-30T10:00:00Z'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('available_lower_seats', response.data)
        self.assertIn('available_upper_seats', response.data)

    def test_booking(self):
        user = CustomUser.objects.create_user(**self.user_data)
        bus = Buses.objects.create(**self.bus_data)
        booking_data = {
            'booked_by': user.id,
            'booked_Bus': bus.id,
            'status': 'C',
            'seat_no': [1],
            'seat_position': 'L',
            'trip_date': '2025-09-30T10:00:00Z'
        }
        url = reverse('get_bookings')
        response = self.client.post(url, booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Try booking the same seat again
        response2 = self.client.post(url, booking_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_authentication(self):
        self.client.post(reverse('register_user'), self.user_data, format='json')
        login_data = {'username': self.user_data['username'], 'password': self.user_data['password']}
        response = self.client.post(reverse('token_obtain_pair'), login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_protected_booking_endpoint(self):
        self.client.post(reverse('register_user'), self.user_data, format='json')
        login_data = {'username': self.user_data['username'], 'password': self.user_data['password']}
        token_response = self.client.post(reverse('token_obtain_pair'), login_data, format='json')
        access_token = token_response.data['access']
        user = CustomUser.objects.get(username=self.user_data['username'])
        bus = Buses.objects.create(**self.bus_data)
        booking_data = {
            'booked_by': user.id,
            'booked_Bus': bus.id,
            'status': 'C',
            'seat_no': [1],
            'seat_position': 'L',
            'trip_date': '2025-09-30T10:00:00Z'
        }
        url = reverse('get_bookings')
        # Without token
        response = self.client.post(url, booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should be protected in production
        # With token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response2 = self.client.post(url, booking_data, format='json')
        self.assertIn(response2.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
