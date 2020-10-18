from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from discovery import DiscoveryClient

discovery = DiscoveryClient()


class GameViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'

    @action(detail=False, methods=['POST'])
    def recommendations(self, request):
        query = ''
        for tag in request.data['tags']:
            query += 'keywords.slug:\"{slug}\"|' \
                    'summary:\"{slug}\"|' \
                    'genres.slug:\"{slug}\"|' \
                    'themes.slug:\"{slug}\"|'.format(slug=tag)
        # Remove trailing pipe
        query = query[:len(query) - 1]

        games_list = discovery.query(
            collection_id=settings.DISCOVERY_COLLECTION_ID,
            environment_id=settings.DISCOVERY_ENVIRONMENT_ID,
            query=query)['results']
        results = []
        for game in games_list:
            results.append({"name": game['name'], "summary": game['summary'], "cover": game['cover'],
                            "slug": game['slug']})
        return Response(results)

    def retrieve(self, request, slug=None, **kwargs):
        game = discovery.query(
            collection_id=settings.DISCOVERY_COLLECTION_ID,
            environment_id=settings.DISCOVERY_ENVIRONMENT_ID,
            filter="slug::" + slug)['results'][0]
        return Response(game)
