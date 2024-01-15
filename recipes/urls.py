from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientListCreateView, IngredientRetrieveUpdateDestroyView, IngredientViewSet, MyRecipeListView, RecipeViewSet, RecipeListView, TopIngredientsView

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'', RecipeViewSet, basename='recipe')
urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('myrecipes/', MyRecipeListView.as_view(), name='myrecipe-list'),
    path('top-ingredients/', TopIngredientsView.as_view(), name='top-ingredients'),
    path('', include(router.urls)),
    
]