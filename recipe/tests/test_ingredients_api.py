from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicIngredientsApiTests(TestCase):
    """Test public ingredient api"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_ingredients_unauthenticated(self):
        """Test that authentication is required for getting ingredients"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test API requests that requires authentication"""

    def setUp(self) -> None:
        self.user = create_user(
            email='demo@demo.com',
            password='123456',
            name='test name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_ingredients_successful(self):
        """Test that getting ingredients is successful"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Sault')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test ingredients returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'user2@demo.com',
            '123456'
        )
        Ingredient.objects.create(user=user2, name='Vinegar')
        ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_add_Ingredient_successful(self):
        """Test that adding a Ingredient is successful"""
        payload = {'name': 'test Ingredient'}
        self.client.post(INGREDIENTS_URL, payload)

        # self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_add_Ingredient_invalid(self):
        """Test that Ingredient name is required"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_ingredients_assigned_to_recipes(self):
        """Test filter ingredients by those assigned to recipes"""
        ingredient1 = Ingredient.objects.create(user=self.user,
                                                name='ingredient one')
        ingredient2 = Ingredient.objects.create(user=self.user,
                                                name='ingredient two')
        recipe = Recipe.objects.create(
            user=self.user,
            title='test recipe',
            time_minutes=10,
            price=5.00
        )
        recipe.ingredients.add(ingredient1)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
