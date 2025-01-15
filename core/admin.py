from django.contrib import admin
from .models import Movie, Theatre, Screen, Seat, Screening, Booking, Row, ExtendedBooking

admin.site.site_header = "Booker Admin Portal"
admin.site.site_title = "Booker Admin Portal"
admin.site.index_title = "Welcome to Booker Portal"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date', 'duration')
    search_fields = ("title",)
    list_filter = ("release_date",)


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    search_fields = ("name", "location")


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ('screen', 'name', 'seat_count')
    search_fields = ('screen',)


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ("name", "theatre", "total_seats")
    search_fields = ("name", "theatre__name")
    list_filter = ("theatre",)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("screen", "row", "number")
    search_fields = ("screen__name", "row", "number")
    list_filter = ("screen", "row")
    ordering = ("screen", "row", "number")


@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ("movie", "screen", "start_time")
    search_fields = ("movie__title", "screen__name")
    list_filter = ("movie", "screen__theatre", "start_time")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "screening", "booked_at")

@admin.register(ExtendedBooking)
class BookingAdmin(admin.ModelAdmin):
    pass

