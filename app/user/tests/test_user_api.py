from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Tests public user apis"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_valid(self):
        """tests creating a user with valid params successfully"""

        params = {
            'email': 'test@email.com',
            'password': 'demo1234',
            'name': 'Test User'
        }

        res = self.client.post(
            CREATE_USER_URL,
            params
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(params['password']))
        self.assertNotIn(params['password'], res.data)

    def test_user_exists(self):
        """Test and fail when user already exists"""

        params = {
            'email': 'test@email.com',
            'password': 'demo1234',
            'name': 'Test User'
        }

        create_user(**params)

        res = self.client.post(
            CREATE_USER_URL,
            params
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_length_short(self):
        """Tests if a password shorther then needed"""

        params = {
            'email': 'test@email.com',
            'password': '1234',
            'name': 'Test User'
        }

        res = self.client.post(
            CREATE_USER_URL,
            params
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=params['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        """Test that a token is created for user"""

        params = {
            'email': 'test@email.com',
            'password': 'demo1234',
            'name': 'Test User'
        }

        create_user(**params)
        res = self.client.post(TOKEN_URL, params)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """Test that a token is not created for invalid user credentials"""

        params = {
            'email': 'test@email.com',
            'password': 'demo1234',
            'name': 'Test User'
        }

        create_user(**params)
        params['password'] = 'wrongpassword'
        res = self.client.post(TOKEN_URL, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user(self):
        """Test that a token is not created for non-existing user"""

        params = {
            'email': 'test@email.com',
            'password': 'demo1234',
            'name': 'Test User'
        }

        res = self.client.post(TOKEN_URL, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
