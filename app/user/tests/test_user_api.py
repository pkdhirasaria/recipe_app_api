from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Helper Function for create user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    def setUP(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'lightyagami@deathnote.com',
            'password': 'testpass',
            'name': 'Light Yagami'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test Creating user that already exists fails"""

        payload = {
            'email': 'lightyagami@deathnote.com',
            'password': 'testpass',
            'name': 'Light Yagami'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Password must be more than 5 characters"""

        payload = {
            'email': 'lightyagami@deathnote.com',
            'password': 'test',
            'name': 'Light Yagami'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exsts = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exsts)

    def test_create_token_for_user(self):
        """Test that a token is created for user"""
        payload = {
            'email': 'lightyagami@deathnote.com',
            'password': 'testpass'
        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_invalid_credentials(self):
        """Test that token is not created if invalid credentails are given"""
        payload = {
            'email': 'lightyagami@deathnote.com',
            'password': 'testpass'
        }

        create_user(**payload)

        payload = {
            'email': 'lightyagami@deathnote.com',
            'password': 'wrong'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that chceck toekn not created if user not created"""

        payload = {
            'email': 'lightyagami@deathnote.com',
            'password': 'testpass'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and passsword are required"""

        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
