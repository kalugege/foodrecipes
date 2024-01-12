from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import MyUser
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Wrong Credentials"}, status=400)

class UserListView(APIView):
    def get(self, request, *args, **kwargs):
        users = MyUser.objects.all()
        serializer = UserRegistrationSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(MyUser, id=user_id)
        serializer = UserRegistrationSerializer(user)
        return Response(serializer.data)