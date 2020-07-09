from django.db import models

from accounts.models import User

class FoodQuerySet(models.QuerySet):
    pass

class FoodManager(models.Manager):
    def get_queryset(self):
        return FoodQuerySet(self.model, using=self._db)

class Dish(models.Model):

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


class Order(models.Model):

    ORDER_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
        ]

    customer_name      = models.ForeignKey(User, on_delete=models.CASCADE)
    time_of_order      = models.DateTimeField(auto_now_add=True)
    updated            = models.DateTimeField(auto_now=True)
    address            = models.TextField()
    dish               = models.ForeignKey('Dish', on_delete=models.CASCADE)
    qty                = models.IntegerField()
    total_cost         = models.IntegerField()
    payment_status     = models.CharField(max_length=15, choices=ORDER_CHOICES)

    objects = FoodManager()

    def __str__(self):
        return str(self.dish.name)



class PaymentHistory(models.Model):

    PAYMENT_CHOICES = [
    ('Success', 'Success'),
    ('Failed', 'Failed'),
    ('Pending', 'Pending'),
        ]

    the_order          = models.OneToOneField(Order, on_delete=models.CASCADE)
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