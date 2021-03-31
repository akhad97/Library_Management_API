from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token

# User = get_user_model()


# class LibraryUserSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = LibraryUser
#         fields = ('id', 'full_name', 'email', 'username')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'bookname', 'authorname', 'category')


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'bookname', 'authorname', 'category', 'barcode')


class BookOrderSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    def save(self):
        book = self.validated_data['book']
        user = self.context['request'].user
        # lib_user = LibraryUser.objects.filter(user=user)
        order, created = BookOrder.objects.get_or_create(user=user)
        if order.books.filter(id=book.id):
            raise serializers.ValidationError('Book already loaned')
        order.books.add(book)
        return order

class ReturnBookSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    def remove(self):
        book = self.validated_data['book']
        user = self.context['request'].user
        order, created = BookOrder.objects.get_or_create(user=user)
        if not order.books.filter(id=book.id):
            raise serializers.ValidationError('Book not loaned')
        order.books.remove(book)
        return order


class EmptySerializer(serializers.Serializer):
    pass


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)
    

class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'auth_token')
         read_only_fields = ('id', 'is_active', 'is_staff', 'auth_token')
    
    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key    


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')

    def validate_email(email, value):
        user = User.objects.filter(username=email)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value