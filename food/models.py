from django.db import models

class DishQuerySet(models.QuerySet):
    pass

class DishManager(models.Manager):
    def get_queryset(self):
        return DishQuerySet(self.model, using=self._db)

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

    objects = DishManager()

    def __str__(self):
        return self.name