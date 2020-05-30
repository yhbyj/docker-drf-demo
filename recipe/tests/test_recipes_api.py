from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='test tag'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='test ingredient'):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **kwargs):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(kwargs)
    return Recipe.objects.create(user=user, **defaults)


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicRecipesApiTests(TestCase):
    """Test public recipe api"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_recipes_unauthenticated(self):
        """Test that authentication is required for getting recipes"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesApiTests(TestCase):
    """Test API requests that requires authentication"""

    def setUp(self) -> None:
        self.user = create_user(
            email='demo@demo.com',
            password='123456',
            name='test name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_recipes_successful(self):
        """Test that getting recipes is successful"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test recipes returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'user2@demo.com',
            '123456'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = sample_recipe(self.user)
        recipe.tags.add(sample_tag(self.user))
        recipe.ingredients.add(sample_ingredient(self.user))
        serializer = RecipeDetailSerializer(recipe)

        res = self.client.get(detail_url(recipe.id))

        self.assertEqual(res.data, serializer.data)

    # def test_add_recipe_successful(self):
    #     """Test that adding a recipe is successful"""
    #     payload = {'title': 'test recipe'}
    #     self.client.post(RECIPES_URL, payload)
    #
    #     exists = Recipe.objects.filter(
    #         user=self.user,
    #         title=payload['title']
    #     ).exists()
    #     self.assertTrue(exists)
    #
    # def test_add_recipe_invalid(self):
    #     """Test that recipe title is required"""
    #     payload = {'title': ''}
    #     res = self.client.post(RECIPES_URL, payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
