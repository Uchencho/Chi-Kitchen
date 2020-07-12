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


class OrderEntry(models.Model):
    """
    Stores orders' entry, not details. The bridge between order info
    and payment history
    """

    ORDER_STATUS = [
    ('Success', 'Success'),
    ('Failed', 'Failed'),
    ('Pending', 'Pending'),
        ]

    customer_name      = models.ForeignKey(User, on_delete=models.CASCADE)
    status             = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')
    time_of_order      = models.DateTimeField(auto_now_add=True)
    dish               = models.TextField(help_text='List of dishes')
    total_cost         = models.IntegerField()
    payment_ref        = models.CharField(max_length=50)

    objects = FoodManager()



class PaymentHistory(models.Model):
    """
    Stores payment history of each order
    """

    PAYMENT_CHOICES = [
    ('Success', 'Success'),
    ('Failed', 'Failed'),
    ('Pending', 'Pending'),
        ]

    order_info         = models.ForeignKey(OrderEntry, on_delete=models.CASCADE)
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
    Stores orders details that payment has been confirmed
    """

    order_info         = models.ForeignKey(OrderEntry, on_delete=models.CASCADE)
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
# When user is ready to pay: 
    # items in cart are summend up for payment
    # Here we create an order entry, create orders list and one payment entry
    # items are deleted from cart
# On confirmation of payment, set status to successful


# Callback url will be handled by client
# Create a verify payment view that takes in ref id
# This view will determine if a user will initiate another payment

# How to handle try again?

# Order ID and Order Info
# Order ID is tied to Order Info and Order ID is tied to payment


# Back office
# To see which orders to dispatch on a specific day
# Query orderEntry table, filtering all successful transcations
# Use that to do a join on orders table, further filtering delivery date
# Hence you have successful transactions on a given day