from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from django.utils import timezone

from food.models import Dish, Cart, OrderEntry, PaymentHistory, OrderInfo

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
            'email' : 'peter@gmail.com',
            'password' : 'chefchi'
        }
        url_token = api_reverse('api-accounts:login')

        token_response = self.client.post(url_token, token_data, format='json')
        token = token_response.data.get("access", 0)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Create dishes
        Dish.objects.bulk_create([
            Dish(name = "Fried Rice",
            price = 2500,
            dish_type = "Lunch",
            date_available = "2020-07-17",
            tag = 'Grains'),

            Dish(name = "Pounded Yam and Egusi Soup",
            price = 4500,
            dish_type = "Dinner",
            date_available = "2020-07-18",
            tag = 'Swallow'),
        ])

    def test_a_add_items_to_cart(self):
        data = [{
            "dish": "Fried Rice",
            "delivery_date": "2020-07-17",
            "address": "Lagos",
            "qty": 3
            }
        ]

        cart_url = api_reverse('api-food:addCart')
        cart_response = self.client.post(cart_url, data, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        
    def test_b_edit_added_items_in_cart(self):
        data = [{
            "dish": "Fried Rice",
            "delivery_date": "2020-07-17",
            "address": "Lagos",
            "qty": 3
            }
        ]

        cart_url = api_reverse('api-food:addCart')
        cart_response = self.client.post(cart_url, data, format='json')

        edit_data = {
            "dish": "Fried Rice",
            "delivery_date": "2020-07-17",
            "address": "Maitaima Abuja",
            "qty": 1
            }
            
        edit_url = api_reverse('api-food:editcart', kwargs={"pk":1})
        edit_response = self.client.patch(edit_url, edit_data, format='json')
        self.assertEqual(edit_response.status_code, status.HTTP_200_OK)

    def test_c_delete_item_added_to_cart(self):
        data = [{
            "dish": "Fried Rice",
            "delivery_date": "2020-07-17",
            "address": "Lagos",
            "qty": 3
            }
        ]

        cart_url = api_reverse('api-food:addCart')
        cart_response = self.client.post(cart_url, data, format='json')
            
        del_url = api_reverse('api-food:editcart', kwargs={"pk":1})
        del_response = self.client.delete(del_url)
        self.assertEqual(del_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.count(), 0)

    def test_d_order_multiple_dishes_with_one_request(self):
        data = [{
            "dish": "Fried Rice",
            "delivery_date": "2020-07-17",
            "address": "Lagos",
            "qty": 3
            },
            {
            "dish": "Pounded Yam and Egusi Soup",
            "delivery_date": "2020-07-18",
            "address": "Abuja",
            "qty": 2
            },
        ]

        cart_url = api_reverse('api-food:addCart')
        cart_response = self.client.post(cart_url, data, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 2)

    def test_e_view_items_added_to_cart(self):
        data = [{
            "dish": "Fried Rice",
            "delivery_date": "2020-07-17",
            "address": "Lagos",
            "qty": 3
            },
            {
            "dish": "Pounded Yam and Egusi Soup",
            "delivery_date": "2020-07-18",
            "address": "Abuja",
            "qty": 2
            },
        ]

        cart_url = api_reverse('api-food:addCart')
        cart_response = self.client.post(cart_url, data, format='json')
        
        view_url = api_reverse('api-food:cart')
        view_response = self.client.get(view_url)
        self.assertEqual(view_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(view_response.json()), 2)


class PaymentAPITestCase(APITestCase):
    def setUp(self):
        # Register this user
        reg_data = {
            "email": "paschal@gmail.com",
            "password": "chefchi",
            "confirm_password": "chefchi"
        }

        url_reg = api_reverse('api-accounts:register')
        register_response = self.client.post(url_reg, reg_data, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        # Login user
        token_data = {
            'email' : 'paschal@gmail.com',
            'password' : 'chefchi'
        }
        url_token = api_reverse('api-accounts:login')

        token_response = self.client.post(url_token, token_data, format='json')
        token = token_response.data.get("access", 0)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Create dishes
        Dish.objects.bulk_create([
            Dish(name = "Fried Rice",
            price = 2500,
            dish_type = "Lunch",
            date_available = "2020-07-17",
            tag = 'Grains'),

            Dish(name = "Pounded Yam and Egusi Soup",
            price = 4500,
            dish_type = "Dinner",
            date_available = "2020-07-18",
            tag = 'Swallow'),
        ])

        # Add item to cart
        data = [{
            "dish": "Fried Rice",
            "delivery_date": "2020-07-17",
            "address": "Lagos",
            "qty": 3
            }
        ]

        cart_url = api_reverse('api-food:addCart')
        cart_response = self.client.post(cart_url, data, format='json')
        self.assertEqual(cart_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        
    def test_a_checkout_payment(self):
        
        view_url = api_reverse('api-food:cart')
        view_response = self.client.get(view_url)

        checkout_url = api_reverse('api-food:checkout')
        checkout_response = self.client.post(checkout_url, view_response.json(), format='json')
        self.assertEqual(checkout_response.status_code, status.HTTP_200_OK)
        self.assertEqual(OrderEntry.objects.count(), 1)
        self.assertEqual(PaymentHistory.objects.count(), 1)

    def test_b_orderEntry_created_after_checkout_payment(self):
        
        view_url = api_reverse('api-food:cart')
        view_response = self.client.get(view_url)

        checkout_url = api_reverse('api-food:checkout')
        self.client.post(checkout_url, view_response.json(), format='json')
        self.assertEqual(OrderEntry.objects.count(), 1)

    def test_c_PaymentHistoryEntry_created_after_checkout_payment(self):
        
        view_url = api_reverse('api-food:cart')
        view_response = self.client.get(view_url)

        checkout_url = api_reverse('api-food:checkout')
        self.client.post(checkout_url, view_response.json(), format='json')
        self.assertEqual(PaymentHistory.objects.count(), 1)

    def test_d_PaymentHistoryView_not_emppty_after_checkout_payment(self):
        
        view_url = api_reverse('api-food:cart')
        view_response = self.client.get(view_url)

        checkout_url = api_reverse('api-food:checkout')
        self.client.post(checkout_url, view_response.json(), format='json')
        
        pay_url = api_reverse('api-food:paymentHistory', kwargs={"pk":1})
        pay_response = self.client.get(pay_url)
        self.assertEqual(pay_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(view_response.json()), 1)

    def test_e_PaymentRetry_after_unsuccessful_checkout_payment(self):

        view_url = api_reverse('api-food:cart')
        view_response = self.client.get(view_url)

        checkout_url = api_reverse('api-food:checkout')
        res = self.client.post(checkout_url, view_response.json(), format='json')
        
        order_url = api_reverse('api-food:orderInfo', kwargs={"pk":1})
        order_response = self.client.get(order_url)

        retry_url = api_reverse('api-food:retrypayment')
        retry_response = self.client.post(retry_url, order_response.json(), format='json')
        self.assertEqual(retry_response.status_code, status.HTTP_200_OK)