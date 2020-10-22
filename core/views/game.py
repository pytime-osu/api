from functools import reduce

from django.conf import settings
from django.db.models import Q, Count
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import ImageTag
from discovery import DiscoveryClient

discovery = DiscoveryClient()


class GameViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'

    @action(detail=False, methods=['POST'])
    def recommendations(self, request):
        query = ''
        for tag in request.data['tags']:
            query += f'keywords.slug:\"{tag}\"|' \
                    f'summary:\"{tag}\"|' \
                    f'genres.slug:\"{tag}\"|' \
                    f'themes.slug:\"{tag}\"|'
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

    @action(detail=False, methods=['POST'])
    def cover_art(self, request):
        game_slugs = request.data.get('games', [])
        search = request.data.get('search', [])
        tag_query = reduce(lambda q, t: q | Q(tag__contains=t), search, Q())
        tags = ImageTag.objects.filter(game__in=game_slugs).filter(tag_query)
        scores = tags.values('game', 'image').annotate(score=Count('tag')).order_by('-score')
        return Response(data=scores)

    def retrieve(self, request, slug=None, **kwargs):
        game = discovery.query(
            collection_id=settings.DISCOVERY_COLLECTION_ID,
            environment_id=settings.DISCOVERY_ENVIRONMENT_ID,
            filter="slug::" + slug)['results'][0]
        return Response(game)
