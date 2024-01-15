# recipe/models.py
from audioop import avg
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.db.models import Count

User = get_user_model()

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    @staticmethod
    def get_top_ingredients():
        return Ingredient.objects.annotate(num_recipes=Count('recipe')).order_by('-num_recipes')[:5]

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    recipe_text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    user_ratings = models.ManyToManyField(get_user_model(), through='Rating', related_name='rated_recipes')
    
    @property
    def average_rating(self):
        return self.rating_set.aggregate(Avg('score'))['score__avg'] or 0.0
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)  
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"{self.score} by {self.user} for {self.recipe}"

    class Meta:
        unique_together = ('recipe', 'user')
