from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib import admin
from django.urls import path, include
from restApi.views import CreateUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("restApi.urls")),
    path('api/user/register/', CreateUserView.as_view(), name='user_registry'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')) 
]
