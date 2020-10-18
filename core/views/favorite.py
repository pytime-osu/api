from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from authentication.models import CustomUser
from core.models import Favorite


class FavoriteViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    @action(detail=False, methods=['POST'])
    def add_favorite(self, request):
        try:
            data = request.data
            username = data['username']
            user = CustomUser.objects.get(username=username)
            slug = data['slug']

            new_entry = Favorite(user=user, slug=slug)
            new_entry.save()

            return Response(status=201)

        except:
            return Response(status=400)

