
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('Staff', 'Staff'),
        ('Librarian', 'Librarian'),
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True)
    student_class = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name if self.name else self.username


class Fees(models.Model):
    FEES_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
        ('Partially Paid', 'Partially Paid'),  # New status for partial payments
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Online Payment', 'Online Payment'),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fee')
    fees_status = models.CharField(max_length=100, choices=FEES_STATUS_CHOICES, null=True)
    paid_date = models.DateField(null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # New field for total amount due
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.fees_status}'


class Books(models.Model):
    BOOK_STATUS_CHOICES = [
        ('Borrowed', 'Borrowed'),
        ('Returned', 'Returned'),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book')
    title = models.CharField(max_length=100, null=True, blank=True)
    book_status = models.CharField(max_length=10, choices=BOOK_STATUS_CHOICES, null=True)
    borrow_date = models.DateField(null=True)
    return_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.title} - {self.book_status}'