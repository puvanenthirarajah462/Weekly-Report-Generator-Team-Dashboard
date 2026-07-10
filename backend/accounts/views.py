from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .serializers import RegisterSerializer, UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds role/user info to the JWT response payload for convenience on the frontend."""

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


@method_decorator(csrf_exempt, name="dispatch")
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    authentication_classes = []


@method_decorator(csrf_exempt, name="dispatch")
class MyTokenRefreshView(TokenRefreshView):
    authentication_classes = []


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserListView(generics.ListAPIView):
    """Used by managers to see all team members (e.g. for filters / project assignment)."""

    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
