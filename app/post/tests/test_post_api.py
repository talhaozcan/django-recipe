from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post, Tag, Content
from post.serializers import PostSerializer, PostDetailSerializer

# /api/post/posts
POST_URL = reverse('post:post-list')


# /api/post/posts/{id}
def post_detail_url(post_id):
    """return detail url for a post"""
    return reverse('post:post-detail', args=[post_id])


def create_tag(user, name='Sample Tag'):
    """create sample tag"""
    return Tag.objects.create(user=user, name=name)


def create_content(user, title='Sample Content', text=''):
    """create sample content"""
    return Content.objects.create(user=user, title=title, text=text)


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

    def test_retrieve_post_detail(self):
        """Test retreiving post detail"""

        post = create_post(self.user)
        tag = create_tag(user=self.user)
        content = create_content(user=self.user)
        post.tags.add(tag)
        post.contents.add(content)

        url = post_detail_url(post.id)
        res = self.client.get(url)

        serializer = PostDetailSerializer(post)
        self.assertEqual(res.data, serializer.data)

    def test_create_post(self):
        """Test creating a basic post"""
        params = {
            'post_title': 'Basic Title'
        }

        res = self.client.post(POST_URL, params)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=res.data['id'])
        self.assertEqual(post.post_title, params['post_title'])

    def test_create_post_with_tags(self):
        """Test creating a post with tags"""

        tag1 = create_tag(user=self.user)
        tag2 = create_tag(user=self.user, name='tag2')

        params = {
            'post_title': 'Post with tags',
            'tags': [tag1.id, tag2.id]
        }

        res = self.client.post(POST_URL, params)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=res.data['id'])
        self.assertEqual(post.post_title, params['post_title'])
        self.assertListEqual(
            [t.id for t in post.tags.all()], res.data['tags'])

    def test_create_post_with_content(self):
        """Test creating a post with content"""

        content1 = create_content(user=self.user)

        params = {
            'post_title': 'Post with tags',
            'contents': [content1.id]
        }

        res = self.client.post(POST_URL, params)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=res.data['id'])
        self.assertEqual(post.post_title, params['post_title'])
        self.assertListEqual(
            [c.id for c in post.contents.all()], res.data['contents'])
