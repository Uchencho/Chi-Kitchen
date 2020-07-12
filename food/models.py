from django.db import models

from accounts.models import User

class FoodQuerySet(models.QuerySet):
    pass

class FoodManager(models.Manager):
    def get_queryset(self):
        return FoodQuerySet(self.model, using=self._db)

class Dish(models.Model):
    """
    Stores list of available dish
    """

    DISH_CHOICES = [
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Desert', 'Desert'),
    ('Other', 'Other')
        ]

    name            = models.CharField(max_length=100, unique=True)
    price           = models.IntegerField()
    active          = models.BooleanField(default=True)
    dish_type       = models.CharField(max_length=50, choices=DISH_CHOICES)
    date_available  = models.DateField()
    tag             = models.CharField(max_length=100, blank=True)

    objects = FoodManager()

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'


class Cart(models.Model):
    """
    Stores orders that payment has NOT been received
    """

    customer_name      = models.ForeignKey(User, on_delete=models.CASCADE)
    time_of_order      = models.DateTimeField(auto_now_add=True)
    updated            = models.DateTimeField(auto_now=True)
    delivery_date      = models.DateField()
    address            = models.TextField()
    dish               = models.ForeignKey('Dish', on_delete=models.CASCADE)
    qty                = models.IntegerField()
    total_cost         = models.IntegerField()

    objects = FoodManager()

    def __str__(self):
        return str(self.dish.name)



class PaymentHistory(models.Model):
    """
    Stores payment history of each order
    """

    PAYMENT_CHOICES = [
    ('Success', 'Success'),
    ('Failed', 'Failed'),
    ('Pending', 'Pending'),
        ]

    customer           = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_paid        = models.IntegerField()
    status             = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending')
    authorization_url  = models.URLField(blank=True, null=True)
    access_code        = models.CharField(max_length=200, blank=True, null=True)
    reference          = models.CharField(max_length=200, blank=True, null=True)
    payment_channel    = models.CharField(max_length=200, blank=True, null=True)
    transaction_date   = models.CharField(max_length=200, blank=True, null=True)
    verify_status      = models.CharField(max_length=200, blank=True, null=True)

    objects = FoodManager()

    class Meta:
        verbose_name = 'Paymnet History'
        verbose_name_plural = 'Payment History'



class Order(models.Model):
    """
    Stores orders that payment has been confirmed
    """

    customer_name      = models.ForeignKey(User, on_delete=models.CASCADE)
    time_of_order      = models.DateTimeField(auto_now_add=True)
    delivery_date      = models.DateField()
    address            = models.TextField()
    dish               = models.ForeignKey('Dish', on_delete=models.CASCADE)
    qty                = models.IntegerField()
    total_cost         = models.IntegerField()
    payment_ref        = models.CharField(max_length=50)

    objects = FoodManager()

    def __str__(self):
        return str(self.dish.name)



# Flow has changed, only logged in users can order
# User selects list of dishes he wishes to purchase
# This list is sent to a cart for user to make payment.
# Cart is a table that stores list of orders unpaid for
# When user is ready to pay, items in cart are summend up for payment
# On confirmation of payment, each of those dishes are stored in order table
# an order table for admin to provide service

# payment history table needs to show which orders a user paid for
# Do we create an order on confirmation of payment or on payment
# Once an order is paid for, no refund is possible

# What will be the callback url? Homepage? How will it work

# Response will contain list of orders that payment has been initialized
# with response from paystack
# After payment, user will return to previous tab (no callback)
# Click on verify payment and then we will create the orders if
# payment was successful, also delete the orders from cart 