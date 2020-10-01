from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.response import Response

class Suggestions(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def auto_complete(self,request):
        query = Suggestions.objects.filter(title.startswith("serachbar entry"))
        res = []
        for result in query:
            res.append(result.content)
        return Response(results)
