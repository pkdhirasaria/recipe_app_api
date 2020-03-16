from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):

    def test_create_uesr_with_email_successful(self):
        """Test Creating a new user with an email is sucessful"""
        email = "lightyagami@deathnote.com"
        password = 'LightYagami'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is test_new_user_email_normalized"""

        email = "lightyagami@DEATHNOTE.COM"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""

        user = get_user_model().objects.create_superuser(
            'lightyagami@deathnote.com',
            'test@123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
