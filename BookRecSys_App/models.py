from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=80)
    id = models.AutoField(primary_key=True, auto_created=True)  # userid


class Book(models.Model):
    isbn = models.CharField(max_length=254, unique=True, primary_key=True)
    title = models.CharField(max_length=254)
    author = models.CharField(max_length=254)
    year = models.IntegerField()
    publisher = models.CharField(max_length=254)
    image_url = models.CharField(max_length=254)
    rating_count = models.IntegerField()


class Rating(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)  # userid
    title = models.CharField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


class Dislike(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)  # userid
    title = models.CharField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)