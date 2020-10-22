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
        try:
            data = request.data
            print(data)
            username = data['username']
            user = CustomUser.objects.get(username=username)
            slug = data['slug']

            new_entry = Favorite(user=user, slug=slug)
            new_entry.save()

            return Response(status=201)

        except:
            return Response(status=400)

    @action(detail=False, methods=['POST'])
    def get_favorites(self, request):
        data = request.data
        username = data['username']
        user = CustomUser.objects.get(username=username)
        favorites = Favorite.objects.filter(user=user).values()
        games = []
        for entry in list(favorites):
            slug = entry['slug']
            query = "slug::\"{unique}\"".format(unique=slug)

            games_list = discovery.query(
                collection_id=settings.DISCOVERY_COLLECTION_ID,
                environment_id=settings.DISCOVERY_ENVIRONMENT_ID,
                query=query)['results']

            for game in games_list:
                games.append({"name": game['name'], "summary": game['summary'], "cover": game['cover'],
                              "slug": game['slug']})

        return Response(games)
