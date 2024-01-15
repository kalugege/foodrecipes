from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from users.models import MyUser
from .models import Ingredient, Rating, Recipe
from .serializers import IngredientSerializer, RecipeSerializer
from rest_framework.test import APITestCase
from rest_framework import status

class RecipeViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = MyUser.objects.create_user(email='testuser@example.com', password='testpass', first_name='Test', last_name='User')
        self.client.force_authenticate(user=self.test_user)

    def test_list_recipes(self):
        response = self.client.get(reverse('recipe-list'))
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class IngredientViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = MyUser.objects.create_user(email='testuser@example.com', password='testpass', first_name='Test', last_name='User')
        self.client.force_authenticate(user=self.test_user)

    def test_list_ingredients(self):
        response = self.client.get(reverse('ingredient-list'))
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class RecipeTests(APITestCase):
    def setUp(self):
        self.test_user = MyUser.objects.create_user(email='testuser@example.com', password='testpass',first_name='Test', last_name='User')
        self.client.force_authenticate(user=self.test_user)  # authenticate the user
        self.ingredient = Ingredient.objects.create(name='Test Ingredient')

    # def test_create_recipe(self):
    #     url = reverse('recipe-list')
    #     data = {'name': 'Test Recipe', 'recipe_text': 'Some text', 'ingredients': [self.ingredient]}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Recipe.objects.count(), 1)
    #     self.assertEqual(Recipe.objects.get().name, 'Test Recipe')
