from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from authentication.models import CustomUser
from core.models import Favorite
from discovery import DiscoveryClient

discovery = DiscoveryClient()


class FavoriteViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    @action(detail=False, methods=['POST'])
    def add_favorite(self, request):
        data = request.data
        username = data['username']
        user = CustomUser.objects.get(username=username)
        slug = data['slug']
        if Favorite.objects.filter(user=user, slug=slug).exists():
            return Response(status=400)

        else:
            new_entry = Favorite(user=user, slug=slug)
            new_entry.save()
            return Response(status=201)

    @action(detail=False, methods=['POST'])
    def is_favorite(self, request):
        data = request.data
        username = data['username']
        user = CustomUser.objects.get(username=username)
        slug = data['slug']
        if Favorite.objects.filter(user=user, slug=slug).exists():
            return Response({'is_favorite': True})

        else:
            return Response({'is_favorite': False})

    @action(detail=False, methods=['POST'])
    def get_favorites(self, request):
        data = request.data
        username = data['username']
        user = CustomUser.objects.get(username=username)
        favorites = Favorite.objects.filter(user=user).values()
        shows = []
        for entry in list(favorites):
            slug = entry['slug']
            query = "name::\"{unique}\"".format(unique=slug)

            shows_list = discovery.query(
                collection_id=settings.DISCOVERY_COLLECTION_ID,
                environment_id=settings.DISCOVERY_ENVIRONMENT_ID,
                query=query)['results']

            for show in shows_list:
                shows.append({"name": show['name'], "summary": show['overview'], "cover": show['poster_path']})

        return Response(shows)

    @action(detail=False, methods=['POST'])
    def remove_favorite(self, request):
        data = request.data
        username = data['username']
        user = CustomUser.objects.get(username=username)
        slug = data['slug']
        if (Favorite.objects.filter(user=user, slug=slug).delete())[0] == 1:
            return Response(status=201)

        else:
            return Response(status=400)
