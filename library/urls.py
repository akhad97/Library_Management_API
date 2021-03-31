from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'api', views.AuthViewSet, basename='api')


urlpatterns = [
    path('', include(router.urls)),
    path('book-list/', views.BookList.as_view()),
    path('book-detail/<int:pk>/', views.BookDetail.as_view()),
    path('orders/', views.BookOrderList.as_view()),
    path('book-order/', views.BookOrder.as_view()),
    path('book-return/', views.ReturnBook.as_view()),

    path('api-auth/', include('rest_framework.urls', namespace='rest-framework')),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
