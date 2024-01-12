from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from .models import Rating, Recipe
from .serializers import RatingSerializer, RecipeSerializer
from recipes import serializers
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

class RecipeCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(request.headers)
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RatingCreateView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.validated_data['recipe'].creator == self.request.user:
            raise serializers.ValidationError("You cannot rate your own recipe.")
        serializer.save(user=self.request.user)
