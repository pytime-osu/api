from rest_framework.response import Response
from rest_framework.decorators import api_view
from discovery import DiscoveryClient
from django.conf import settings
import json

discovery = DiscoveryClient()


# Create your views here.
@api_view(['POST'])
def rec_list(request):
    if request.method == 'POST':
        tag = request.data['tag']
        games_list = discovery.query(
            collection_id=settings.DISCOVERY_COLLECTION_ID,
            environment_id=settings.DISCOVERY_ENVIRONMENT_ID,
            natural_language_query=tag)['results']
        results = []
        for game in games_list:
            results.append({"name": game['name'], "summary": game['summary'], "cover_url": game['cover']['url'],
                            "slug": game['slug']})

        return Response(results)


@api_view(['POST'])
def game_detail(request):
    if request.method == 'POST':
        id = request.data['slug']
        game = discovery.query(
            collection_id=settings.DISCOVERY_COLLECTION_ID,
            environment_id=settings.DISCOVERY_ENVIRONMENT_ID,
            filter="slug::" + id)['results']

        return Response(game)
