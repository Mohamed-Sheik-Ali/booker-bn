from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Theatre, Screen, Screening, Seat, Booking, ExtendedBooking
import json
from datetime import datetime


class ExtendedBookingTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@example.com')

        # Create a movie
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='A test movie',
            duration='120 mins',
            genre='Action',
            release_date=datetime.now()
        )

        # Create a theatre
        self.theatre = Theatre.objects.create(name='Test Theatre', location='Test Location')

        # Create a screen
        self.screen = Screen.objects.create(theatre=self.theatre, name='Screen 1', total_seats=100)

        # Create a screening
        self.screening = Screening.objects.create(
            movie=self.movie,
            screen=self.screen,
            start_time=datetime.now()
        )

    def test_calculate_total_price(self):
        # Create an ExtendedBooking instance
        booked_seats = json.dumps([{'row': 'A', 'number': 1}, {'row': 'A', 'number': 2}])
        extended_booking = ExtendedBooking.objects.create(
            user=self.user,
            screening=self.screening,
            booked_seats=booked_seats
        )

        # Calculate the total price
        price_per_seat = 150.00
        total_price = extended_booking.calculate_total_price(price_per_seat)

        # Check if the total price is correct
        self.assertEqual(total_price, 300.00)

    def test_save_updates_total_price(self):
        # Create an ExtendedBooking instance
        booked_seats = json.dumps([{'row': 'A', 'number': 1}, {'row': 'A', 'number': 2}])
        extended_booking = ExtendedBooking.objects.create(
            user=self.user,
            screening=self.screening,
            booked_seats=booked_seats
        )

        # Check if the total price is updated correctly when saving
        extended_booking.save()
        self.assertEqual(extended_booking.total_price, 300.00)