from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='Quiz App Swagger')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library.urls')),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # path('docs/', schema_view),
]
