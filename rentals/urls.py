from django.urls import path
from .views import (
    UserCreateAPIView,
    LoginAPIView,
    RentalAPIView,
    ExtendRentalAPIview,
    AllBookAPIView,
    BookAPIView,
    RentalBookFeeAPI,
    UserAllRentalBooksAPI,
)

urlpatterns = [
    path("user/", UserCreateAPIView.as_view(), name="user_create"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("all-books/", AllBookAPIView.as_view(), name="book_list"),
    path("books/", BookAPIView.as_view(), name="books"),
    path("rentals/", RentalAPIView.as_view(), name="rentals"),
    path("extend/<int:pk>/", ExtendRentalAPIview.as_view(), name="extend_rental"),
    # UserAllRentalBooksAPI
    path('user-rentals/', UserAllRentalBooksAPI.as_view(), name='user_rentals'),
    path("rental-fee/<int:pk>/", RentalBookFeeAPI.as_view(), name="rental_fee"),
]
