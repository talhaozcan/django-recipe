from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post
from post.serializers import PostSerializer

POST_URL = reverse('post:post-list')


def create_post(user, **params):
    """create sample post"""
    sample = {
        'post_title': 'Sample Post',
    }
    sample.update(params)

    return Post.objects.create(user=user, **sample)


class PublicPostApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to list the posts"""
        res = self.client.get(POST_URL)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostTests(TestCase):

    def setUp(self):
        params = {
            'email': 'test@email.com',
            'password': 'demo1234',
            'name': 'Test User'
        }
        self.user = get_user_model().objects.create_user(**params)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retreive_post(self):
        """test retreiving list of posts"""

        create_post(user=self.user)
        create_post(user=self.user)

        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)

        res = self.client.get(POST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_posts_limited_to_user(self):
        """Test retrieving posts belong to the specific user"""

        user2 = get_user_model().objects.create_user(
            email='test2@email.com',
            password='demo1234'
        )
        post = create_post(user=self.user)
        new_post = {'post_title': 'Second Sample'}
        create_post(user=user2, **new_post)
        res = self.client.get(POST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['post_title'], post.post_title)
