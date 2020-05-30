# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/29 9:11'

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicTagsApiTests(TestCase):
    """Test public tag api"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_tags_unauthenticated(self):
        """Test that authentication is required for getting tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test API requests that requires authentication"""

    def setUp(self) -> None:
        self.user = create_user(
            email='demo@demo.com',
            password='123456',
            name='test name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_tags_successful(self):
        """Test that getting tags is successful"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test tags returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'user2@demo.com',
            '123456'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_add_tag_successful(self):
        """Test that adding a tag is successful"""
        payload = {'name': 'test tag'}
        self.client.post(TAGS_URL, payload)

        # self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_add_tag_invalid(self):
        """Test that tag name is required"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
