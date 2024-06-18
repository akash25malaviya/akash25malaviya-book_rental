from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer,
    BookSerializer,
    LoginSerializer,
    RentalSerializer,
)
from .models import Book, Rental
import requests


def get_book_details(title):
    url = f"https://openlibrary.org/search.json?title={title}"
    response = requests.get(url)
    data = response.json()

    if data["docs"]:
        book_data = data["docs"][0]
        return {
            "title": book_data.get("title"),
            "author": ", ".join(book_data.get("author_name", [])),
            "page_count": book_data.get("number_of_pages_median", 0),
        }
    return None


class UserCreateAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            response_data = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "tokens": user.tokens,
            }
            return Response(
                {
                    "status": True,
                    "message": "Login successfully",
                    "data": response_data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "status": True,
                    "message": "Somthig wont's wrong",
                    "data": {},
                },
                status=status.HTTP_201_CREATED,
            )


class RentalAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        rentals = Rental.objects.all()
        serializer = RentalSerializer(rentals, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        data["end_date"] = date.today() + timedelta(days=30)
        if Rental.objects.filter(user=data["user"], book=data["book"]).exists():
            return Response(
                {"message": "You have already rented this book"}, status=400
            )
        serializer = RentalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ExtendRentalAPIview(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        rental = Rental.objects.get(pk=pk)
        rental.extended = True
        rental.end_date = date.today() + timedelta(days=30)
        rental.calculate_fee()
        rental.save()
        return Response({"message": "Rental extended successfully"}, status=200)


class AllBookAPIView(generics.GenericAPIView):
    def get(self, request):
        books = Book.objects.all().values()
        response = {"message": "books found", "books": books}
        return Response(response)


class BookAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        title = request.data.get("title")
        if not title:
            return Response(
                {"title": "This field is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        book_data = get_book_details(title)
        if book_data:
            Book.objects.update_or_create(**book_data)
            return Response({"msg": "book added"}, status=status.HTTP_201_CREATED)
        return Response({"msg": "book not found"}, status=status.HTTP_404_NOT_FOUND)


class RentalBookFeeAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        rental = Rental.objects.get(pk=pk)
        return Response({"fee": rental.fee})
    
class UserAllRentalBooksAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        rentals = Rental.objects.filter(user=request.user).values()
        return Response(rentals)