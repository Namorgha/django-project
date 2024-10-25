from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', Home.as_view(), name='api_home'),                    # Home view with JWT auth
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT Token obtain
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   # JWT Token refresh
    path('logout/', LogoutView.as_view(), name='logout'),     # Blacklist refresh token on logout
    path('protected/', ProtectedView.as_view(), name='protected'), # Example protected route
]
