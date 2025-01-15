from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from .serializers import RegisterSerializer, LoginSerializer, MovieSerializer, ScreenWithSeatSerializer, \
    ScreenSerializer, BookingSerializer, BookingHistorySerializer
from .models import Movie, Screen, Booking, Screening


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user, created = User.objects.get_or_create(email=request.data['email'])
            user.set_password(request.data['password'])
            user.save()

            token, token_created = Token.objects.get_or_create(user=user)

            return Response({
                "message": "User registered successfully!",
                "token": token.key,
                "data": serializer.data,
                "status": True
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


USER_KEY = 'user_data'


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response({"status": False, "data": "Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        serializer = self.serializer_class(user)

        user_data = cache.get(USER_KEY)
        user_detail = None
        if not user_data:
            print('NO CACHE')
            user_detail = serializer.data
            cache.set(USER_KEY, serializer.data)
        else:
            user_detail = cache.get(USER_KEY)
            print('CACHED')

        return Response({
            "status": True,
            "token": token.key,
            "data": user_detail,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()

            return Response({"message": "Logged out successfully!"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "No token found for the user."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def get(self, request, id=None):
        if id is None:
            movies = Movie.objects.all()
            serializer = MovieSerializer(movies, many=True)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)

        try:
            movie = Movie.objects.get(id=id)
            serializer = MovieSerializer(movie, many=False)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)


class ScreenAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScreenWithSeatSerializer
    queryset = Screen.objects.all()

    def get(self, request, id=None):
        if id is None:
            return Response({'status': False, 'data': 'Id is needed'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            print(id, 'id')
            screen = Screen.objects.get(id=id)
            print(screen, 'SCREEN')
            serializer = ScreenSerializer(screen, many=False)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Screen.DoesNotExist:
            return Response({"error": "Screen not found"}, status=status.HTTP_404_NOT_FOUND)


class BookSeatsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        screening_id = request.data.get("screening_id")
        user_id = request.data.get("user_id")
        seats = request.data.get("seats")
        if not screening_id or not user_id or not seats:
            return Response(
                {"status": False, "message": "screening_id, user_id, and seats are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(seats) > 10:
            return Response(
                {"status": False, "message": "Cannot book more than 10 seats at a time."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            screening = Screening.objects.get(id=screening_id)
        except Screening.DoesNotExist:
            return Response(
                {"status": False, "message": "Screening does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": False, "message": "User does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        existing_bookings = Booking.objects.filter(screening=screening)
        all_booked_seats = [
            seat for booking in existing_bookings for seat in booking.booked_seats_list
        ]

        for seat in seats:
            if seat in all_booked_seats:
                return Response(
                    {"status": False, "message": f"Seat {seat} is already booked."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        booking = Booking(user=user, screening=screening)
        booking.booked_seats_list = seats
        booking.save()

        return Response(
            {"status": True, "message": "Seats booked successfully."},
            status=status.HTTP_200_OK,
        )


class SeatsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get(self, request, screening_id=None):
        if not screening_id:
            return

        try:
            bookings = Booking.objects.filter(screening=screening_id)
            serializer = BookingSerializer(bookings, many=True)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"status": False, "data": 'No Bookings found'}, status=status.HTTP_404_NOT_FOUND)


class BookingHistoryAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingHistorySerializer
    queryset = Booking.objects.all()

    def get(self, request, user_id=None):
        if not user_id:
            return
        try:
            bookings = Booking.objects.filter(user=user_id)
            serializer = BookingHistorySerializer(bookings, many=True)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"status": True, "data": "Bookings not found"}, status=status.HTTP_404_NOT_FOUND)
