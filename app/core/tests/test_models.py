from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class ModelTests(TestCase):

    def test_create_user_via_email(self):
        """Tests creating user with email"""

        email = "user@email.com"
        passwd = "qwe123"

        user = get_user_model().objects.create_user(
            email=email,
            password=passwd
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(passwd))

    def test_create_user_via_invalid_email(self):
        """Test user email validation"""

        no_email = "not_an_email"

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(no_email)

    def test_create_superuser(self):
        """Test creating a new superuser"""

        superuser = get_user_model().objects.create_superuser(
            email="superuser@email.com",
            password="qwe123"
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_stuff)
