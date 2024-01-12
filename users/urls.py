from django.urls import path
from .views import UserDetailView, UserListView, UserRegistrationView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
]
