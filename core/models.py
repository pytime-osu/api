from django.db import models


class Suggestion(models.Model):
    name = models.CharField(max_length=100, unique=True)


class ImageTag(models.Model):
    game = models.CharField(max_length=100)
    image = models.CharField(max_length=50)
    tag = models.CharField(max_length=200)


class Favorite(models.Model):
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE)
    slug = models.CharField(max_length=100)
