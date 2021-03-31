from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import generics, authentication, permissions, status, viewsets

from .models import BookOrder as BookOrderModel
from .utils import get_and_authenticate_user, create_user_account
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.auth import get_user_model, logout, login
from django.core.exceptions import ImproperlyConfigured
from rest_framework import filters
from .pagination import CustomPagination


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['bookname',]


class BookOrder(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookOrderSerializer

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        order = self.serializer.save()
        return Response(status=status.HTTP_200_OK)


class ReturnBook(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = ReturnBookSerializer

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        order = self.serializer.remove()
        return Response(status=status.HTTP_200_OK)


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class BookOrderList(generics.GenericAPIView):
    
    # try:
    def get(self, request):
        return Response(BookOrderModel.objects.get(user=request.user.id).books.values())
    # except BookOrderModel.DoesNotExist():
    #     raise ('fasfs')



class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = EmptySerializer
    queryset = ''
    serializer_classes = {
        'login': UserLoginSerializer,
        'register': UserRegisterSerializer
    }

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

