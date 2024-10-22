from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from expenses.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

class RegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: "User registered successfully",
            400: "Validation errors"
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: UserSerializer,
            404: "User not found"
        }
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise NotFound("User not found")

