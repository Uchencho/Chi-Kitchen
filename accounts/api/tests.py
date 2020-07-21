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
        register_response = self.client.post(url_reg, reg_data, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        token_data = { "email" : "john@gmail.com",
                        "password" : "chefchi"
                            }
        url_token = api_reverse('api-accounts:login')

        token_response = self.client.post(url_token, token_data, format='json')
        token = token_response.data.get("access", 0)
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(token, 0)

    def test_e_refreshToken_returned_on_refresh_request(self):
        reg_data = {
            "email": "john@gmail.com",
            "password": "chefchi",
            "confirm_password": "chefchi"
            }

        url_reg = api_reverse('api-accounts:register')
        register_response = self.client.post(url_reg, reg_data, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        token_data = { "email" : "john@gmail.com",
                        "password" : "chefchi"
                            }
        url_token = api_reverse('api-accounts:login')

        token_response = self.client.post(url_token, token_data, format='json')
        token = token_response.data.get("access", 0)
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(token, 0)


        refresh_data = { "refresh" : token_response.data.get("refresh", 0)}
        self.assertNotEqual(refresh_data['refresh'], 0)

        url_refresh = api_reverse('api-accounts:refresh')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        refresh_response = self.client.post(url_refresh, refresh_data, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(refresh_response.data.get("refresh", 0), 0)

    def test_f_logout_response(self):
        reg_data = {
            "email": "john@gmail.com",
            "password": "chefchi",
            "confirm_password": "chefchi"
            }

        url_reg = api_reverse('api-accounts:register')
        register_response = self.client.post(url_reg, reg_data, format='json')

        token_data = { "email" : "john@gmail.com",
                        "password" : "chefchi"
                            }
        url_token = api_reverse('api-accounts:login')

        token_response = self.client.post(url_token, token_data, format='json')
        token = token_response.data.get("access", 0)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        refresh_data = { "refresh" : token_response.data.get("refresh", 0)}

        url_logout = api_reverse('api-accounts:logout')
        logout_response = self.client.post(url_logout, refresh_data, format='json')
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        url_refresh = api_reverse('api-accounts:refresh')

        refresh_response = self.client.post(url_refresh, refresh_data, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(refresh_response.data.get("refresh", 0), 0)