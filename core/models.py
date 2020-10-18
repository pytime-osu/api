from django.db import models



class Suggestion(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Favorite(models.Model):
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE)
    slug = models.CharField(max_length=100)
