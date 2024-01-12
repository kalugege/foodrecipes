# recipe/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    recipe_text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"{self.score} by {self.user} for {self.recipe}"

    class Meta:
        unique_together = ('recipe', 'user')
