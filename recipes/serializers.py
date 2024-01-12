from rest_framework import serializers
from .models import Recipe
from .models import Rating

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return sum([rating.score for rating in ratings]) / ratings.count()
        return 0

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

    def validate(self, data):
        # Check if the user is trying to rate their own recipe
        if self.context['request'].user == data['recipe'].creator:
            raise serializers.ValidationError("You cannot rate your own recipe.")

        # Check if the user has already rated this recipe
        user = self.context['request'].user
        recipe = data['recipe']
        if Rating.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("You have already rated this recipe.")

        return data