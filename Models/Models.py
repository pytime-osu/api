from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

class Suggestions:
    title = models.CharField(max_length=200)
    content = models.TextField()
    publishDate = models.DateTimeField('date published')

    def __str__(self):
        return self.title