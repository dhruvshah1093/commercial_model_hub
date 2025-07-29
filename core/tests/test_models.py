"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        name = 'Test Name'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test@EXAMPLE.com' , 'test@example.com'],
            ['Test2@Example.com', 'Test2@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'test123', name='Test')
            self.assertEqual(user.email, expected)

    def test_new_user_no_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')


    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'superuser@example.com',
            'test123',
            name='Super User', # how weird is that?
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
