from django.db import models
import json
from django.contrib.auth.models import User as user


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username}"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    poster_image = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    release_date = models.DateTimeField(default=None)

    def __str__(self):
        return self.title


class Theatre(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Screen(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name="screens")
    name = models.CharField(max_length=255)  # Example: "Screen 1"
    total_seats = models.PositiveIntegerField(default=None)

    def __str__(self):
        return f"{self.name} - {self.theatre.name}"


class Row(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="rows")
    name = models.CharField(max_length=5)
    seat_count = models.PositiveIntegerField()

    def __str__(self):
        return f"Row {self.name} in {self.screen.name}"


class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="screenings")
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="screenings")
    start_time = models.DateTimeField(default=None)

    def __str__(self):
        return f"{self.movie.title} at {self.screen.name} on {self.start_time}"


class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="seats", default=None)
    row = models.CharField(max_length=5)
    number = models.PositiveIntegerField(default=None)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('screen', 'row', 'number')

    def __str__(self):
        return f"Seat {self.row}{self.number} in {self.screen.name}"


class Booking(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="bookings", default=None)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, related_name="bookings")
    booked_seats = models.TextField(default=None)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {len(self.booked_seats_list)} seats"

    @property
    def booked_seats_list(self):
        try:
            return json.loads(self.booked_seats)
        except json.JSONDecodeError:
            return []

    @booked_seats_list.setter
    def booked_seats_list(self, value):
        self.booked_seats = json.dumps(value)