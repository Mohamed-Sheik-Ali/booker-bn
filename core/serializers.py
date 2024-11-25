from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Movie, Theatre, Screen, Row, Booking, Seat, Screening
import json


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']  # Add other fields if needed


class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ['name', 'seat_count']


class TheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields = ['name', 'location']


class ScreenSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True, read_only=True)

    class Meta:
        model = Screen
        fields = ['id', 'name', 'total_seats', 'rows']


class ScreeningSerializer(serializers.ModelSerializer):
    screens = ScreenSerializer(many=True, read_only=True)

    class Meta:
        model = Screening
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'


class ScreenWithSeatSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Screen
        fields = ['id', 'name', 'total_seats', 'seats']


class TheatreWithScreensSerializer(serializers.ModelSerializer):
    screens = serializers.SerializerMethodField()

    class Meta:
        model = Theatre
        fields = ['name', 'location', 'screens']

    def get_screens(self, obj):
        screens = obj.screens.all()
        return ScreenSerializer(screens, many=True).data


class MovieSerializer(serializers.ModelSerializer):
    theatres = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_theatres(self, obj):
        screenings = obj.screenings.all()
        theatres_data = {}

        for screening in screenings:
            theatre = screening.screen.theatre

            if theatre.id not in theatres_data:
                theatres_data[theatre.id] = {
                    "id": theatre.id,
                    "name": theatre.name,
                    "location": theatre.location,
                    "screenings": []
                }

            theatres_data[theatre.id]["screenings"].append({
                "id": screening.id,
                "start_time": screening.start_time,
                "screen": {
                    "id": screening.screen.id,
                    "name": screening.screen.name,
                    "total_seats": screening.screen.total_seats
                }
            })

        return list(theatres_data.values())


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'


class BookingHistorySerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()
    theatre = serializers.SerializerMethodField()
    screen = serializers.SerializerMethodField()
    seats = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['movie', 'theatre', 'screen', 'seats', 'date']

    def get_movie(self, obj):
        return obj.screening.movie.title

    def get_theatre(self, obj):
        return obj.screening.screen.theatre.name

    def get_screen(self, obj):
        return obj.screening.screen.name

    def get_seats(self, obj):
        parsed_seats = json.loads(obj.booked_seats)
        return [f"{seat['row']}{seat['number']}" for seat in parsed_seats]

    def get_date(self, obj):
        return obj.booked_at

