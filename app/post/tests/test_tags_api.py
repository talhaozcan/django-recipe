from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from post.serializers import TagSerializer


TAGS_URL = reverse('post:tag-list')


class PublicTagsApiTests(TestCase):
    """Tests for public tags api funtions"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to list the tags"""
        res = self.client.get(TAGS_URL)

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Tests for private(authed) tags api functions"""

    def setUp(self):
        params = {
            'email': 'test@email.com',
            'password': 'demo1234',
            'name': 'Test User'
        }
        self.user = get_user_model().objects.create_user(**params)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='TestTag')
        Tag.objects.create(user=self.user, name='TestTag2')

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_tags_limited_to_user(self):
        """Test retrieving tags belong to the specific user"""

        user2 = get_user_model().objects.create_user(
            email='test2@email.com',
            password='demo1234'
        )
        tag = Tag.objects.create(user=self.user, name='TestTag')
        Tag.objects.create(user=user2, name='TestTag2')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tags_successful(self):
        """Test creating a tag successfully"""

        params = {
            'name': 'tag1',
        }

        res = self.client.post(TAGS_URL, params)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tags_exists = Tag.objects.filter(user=self.user, name='tag1').exists()
        self.assertTrue(tags_exists)

    def test_create_tags_invalid(self):
        """Test creating a tag invalid attrs"""

        params = {
            'name': '',
        }

        res = self.client.post(TAGS_URL, params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
