from django.urls import path
from .views import RecipeCreateView, RatingCreateView

urlpatterns = [
    path('', RecipeCreateView.as_view(), name='recipe-create'),
    path('rate/', RatingCreateView.as_view(), name='recipe-rate'),
]
