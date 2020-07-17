from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from django.utils import timezone

from food.models import Dish

class CartAPITestCase(APITestCase):
    def setUp(self):
        # Register this user
        reg_data = {
            "email": "peter@gmail.com",
            "password": "chefchi",
            "confirm_password": "chefchi"
        }

        url_reg = api_reverse('api-accounts:register')
        register_response = self.client.post(url_reg, reg_data, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        # Login user
        token_data = {
            'username' : 'peter@gmail.com',
            'password' : 'chefchi'
        }
        url_token = api_reverse('api-accounts:login')

        token_response = self.client.post(url_token, token_data, format='json')
        token = token_response.data.get("access_token", 0)
        print(token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Create dishes
        Dish.objects.create(
            name = "Fried Rice",
            price = 2500,
            dish_type = "Lunch",
            date_available = "2020-07-17",
            tag = 'Grains',
        )

    def test_a_add_items_to_cart(self):
        data = [{
            "dish": "Fried Rice",
            "delivery_date": "2020-07-17",
            "address": "Lagos",
            "qty": 3
            }
        ]

        cart_url = api_reverse('api-food:addCart')
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        cart_response = self.client.post(cart_url, data, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_201_CREATED)
        