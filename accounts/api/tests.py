from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status

from accounts.models import User

class AccountAPITestCase(APITestCase):
    def test_a_register_response(self):
        reg_data = {
            "email": "john@gmail.com",
            "password": "chefchi",
            "confirm_password": "chefchi"
            }
        url_reg = api_reverse('api-accounts:register')
        reg_resp = self.client.post(url_reg, reg_data, format='json')
        self.assertEqual(reg_resp.status_code, status.HTTP_201_CREATED)

    def test_b_user_data_created(self):
        reg_data = {
            "email": "john@gmail.com",
            "password": "chefchi",
            "confirm_password": "chefchi"
            }
        url_reg = api_reverse('api-accounts:register')
        self.client.post(url_reg, reg_data, format='json')
        self.assertEqual(User.objects.count(), 1)

    def test_c_duplicate_username_error(self):
        reg_data = {
            "email": "john@gmail.com",
            "password": "chefchi",
            "confirm_password": "chefchi"
            }

        url_reg = api_reverse('api-accounts:register')
        # First post
        self.client.post(url_reg, reg_data, format='json')

        # Second post, which is a duplicate
        duplicate_response = self.client.post(url_reg, reg_data, format='json')
        self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_d_token_returned_on_login(self):
        reg_data = {
            "email": "john@gmail.com",
            "password": "chefchi",
            "confirm_password": "chefchi"
            }

        url_reg = api_reverse('api-accounts:register')
        register_respnse = self.client.post(url_reg, reg_data, format='json')
        self.assertEqual(register_respnse.status_code, status.HTTP_201_CREATED)

        token_data = { "username" : "john@gmail.com",
                        "password" : "chefchi"
                            }
        url_token = api_reverse('api-accounts:login')

        token_response = self.client.post(url_token, token_data, format='json')
        token = token_response.data.get("access_token", 0)
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(token, 0)