import collections
from rest_framework import serializers
from .models import Recipe
from .models import Rating
from .models import Ingredient
from django.db.models import Avg

class RecipeSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    average_rating = serializers.SerializerMethodField()  # change this line
    ingredients = serializers.SlugRelatedField(
        many=True,
        queryset=Ingredient.objects.all(),
        slug_field='name' 
    )

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'recipe_text', 'average_rating', 'creator', 'ingredients']

def get_average_rating(self, obj):
    if isinstance(obj, collections.OrderedDict):
        return None  # or some default value
    ratings = obj.ratings.all().aggregate(Avg('rating'))
    return ratings['rating__avg'] if ratings['rating__avg'] is not None else 0

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].user == data['recipe'].creator:
            raise serializers.ValidationError("You cannot rate your own recipe.")

        user = self.context['request'].user
        recipe = data['recipe']
        if Rating.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("You have already rated this recipe.")

        return data
    
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']