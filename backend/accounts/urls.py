from django.urls import path
from .views import RegisterView, MeView, UserListView, MyTokenObtainPairView, MyTokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", MyTokenRefreshView.as_view(), name="login_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("users/", UserListView.as_view(), name="users"),
]
