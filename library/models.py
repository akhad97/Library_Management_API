from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings


# class LibraryUser(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50, null=True)
#     email = models.EmailField()
#     username = models.CharField(max_length=50)


#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

    # def save(self, *args, **kwargs):
    #     instance = super(LibraryUser, self).save(*args, **kwargs)
    #     return instance
 

class Book(models.Model):
    CATEGORY = (
        ('Education', 'Education'),
        ('Computer', 'Computer'),
        ('Civil', 'Civil'),
        ('Historical', 'Historical')
    )
    bookname = models.CharField(max_length=50)
    authorname = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=CATEGORY, default='Education')

    def __str__(self):
        return self.bookname

def get_expiry():
    return datetime.today() + timedelta(days=10)

class BookOrder(models.Model):
    books = models.ManyToManyField(Book, related_name="books")
    user = models.ForeignKey(User, related_name="users", null=True, on_delete=models.CASCADE)
    orderdate = models.DateTimeField(auto_now_add=True)
    expirydate = models.DateField(default=get_expiry)

    def __str__(self):
        return(self.user.username)




    
   
    
    

