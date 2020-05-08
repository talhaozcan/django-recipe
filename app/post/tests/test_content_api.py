from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework .test import APIClient

from core.models import Content
from post.serializers import ContentSerializer


CONTENT_URL = reverse('post:content-list')


def create_content(**params):
    return Content.objects.create(**params)


class PublicContentApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to list the tags"""
        res = self.client.get(CONTENT_URL)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateContentApiTests(TestCase):

    def setUp(self):
        params = {
            'email': 'test@email.com',
            'password': 'demo1234',
            'name': 'Test User'
        }
        self.user = get_user_model().objects.create_user(**params)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retreive_content(self):
        """Test retrieving a content successfully from a user"""

        params = {
            'title': 'Test Content',
            'text': 'Test content text.',
            'user': self.user,
        }
        params2 = {
            'title': 'Test Content 2',
            'text': 'Test content 2 text.',
            'user': self.user,
        }
        create_content(**params)
        create_content(**params2)

        contents = Content.objects.all().order_by('-title')
        serializer = ContentSerializer(contents, many=True)

        res = self.client.get(CONTENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retreive_content_limited_to_user(self):
        """Test retrieving contents belong to the specific user"""

        user2 = get_user_model().objects.create_user(
            email='test2@email.com',
            password='demo1234'
        )
        params = {
            'title': 'Test Content',
            'text': 'Test content text.',
            'user': self.user,
        }
        params2 = {
            'title': 'Test Content 2',
            'text': 'Test content 2 text.',
            'user': user2,
        }
        content1 = create_content(**params)
        create_content(**params2)

        res = self.client.get(CONTENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], content1.title)

    def test_create_content_successful(self):
        """Test creating a content successfully"""

        params = {
            'title': 'Test Content',
            'text': 'Test content text.',
            'user': self.user,
        }

        res = self.client.post(CONTENT_URL, params)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        content_exists = Content.objects.filter(
            user=self.user, title=params['title']).exists()
        self.assertTrue(content_exists)

    def test_create_content_invalid(self):
        """Test creating a tag invalid attrs"""

        params = {
            'title': '',
        }

        res = self.client.post(CONTENT_URL, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
