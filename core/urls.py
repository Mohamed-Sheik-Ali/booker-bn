from django.urls import path
from .views import RegisterView, LoginView, MovieAPIView, LogoutView, ScreenAPIView, BookSeatsAPIView, SeatsAPIView, BookingHistoryAPIView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register-user'),
    path('auth/login/', LoginView.as_view(), name='login-user'),
    path('auth/logout/', LogoutView.as_view(), name='logout-user'),
    path('movies/', MovieAPIView.as_view(), name='movies-list'),
    path('movies/<int:id>/', MovieAPIView.as_view(), name='movie-detail'),
    path('screen/<int:id>/', ScreenAPIView.as_view(), name='screen'),
    path('book-seats/', BookSeatsAPIView.as_view(), name='booke-seats'),
    path('booked-seats/<int:user_id>/<int:screening_id>/', SeatsAPIView.as_view(), name='booked-seats'),
    path('booking-history/<int:user_id>/', BookingHistoryAPIView.as_view(), name='booking-history')
]