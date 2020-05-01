from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTests(TestCase):

    def setUp(self):

        self.client = Client()

        # admin
        self.admin_user = get_user_model().objects.create_superuser(
            email="superuser@email.com",
            password="qwer1234"
        )

        self.client.force_login(self.admin_user)

        # user

        self.user = get_user_model().objects.create_user(
            email="user@email.com",
            password="qwer4321",
            name="user"
        )

    def test_admin_users_listed(self):
        """Tests if users are listed in users page"""

        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_admin_user_change_page_renders(self):
        """Tests if user change page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_admin_add_page_renders(self):
        """Tests add user page"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
