from django.urls import path
from .views import RegisterAPIView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-details/<int:user_id>/', UserDetailView.as_view(), name='user-details')
]
