from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models

class User(AbstractUser):
    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    pass

class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    page_count = models.IntegerField()

    def __str__(self):
        return self.title

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    extended = models.BooleanField(default=False)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_fee(self):
        if self.extended:
            months_extended = (self.end_date - self.start_date).days // 30
            self.fee = (self.book.page_count / 100) * months_extended
        else:
            self.fee = 0
        self.save()

