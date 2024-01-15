from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from .models import Ingredient, Rating, Recipe
from .serializers import IngredientSerializer, RatingSerializer, RecipeSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(serializer.data.email)
        serializer.save(creator=self.request.user)
    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        if 'score' in request.data:
            recipe = self.get_object()
            score = request.data['score']
            user = request.user

            
            if recipe.creator == user:
                return Response({'message': 'You cannot rate your own recipe.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the score is between 1 and 5
            if score < 1 or score > 5:
                return Response({'message': 'Score must be a number between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                rating = Rating.objects.get(user=user.id, recipe=recipe.id)
                rating.score = score
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except Rating.DoesNotExist:
                # If the user hasn't rated this recipe yet, create a new rating
                rating = Rating.objects.create(user=user, recipe=recipe, score=score)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'You need to provide a score'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
class RecipeListView(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class MyRecipeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        my_recipes = Recipe.objects.filter(creator=request.user)
        serializer = RecipeSerializer(my_recipes, many=True)
        return Response(serializer.data)
    
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
class IngredientListCreateView(ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
class IngredientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
class TopIngredientsView(APIView):
    def get(self, request):
        top_ingredients = Ingredient.get_top_ingredients()
        return Response({"top_ingredients": [ingredient.name for ingredient in top_ingredients]})


