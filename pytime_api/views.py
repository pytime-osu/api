from rest_framework.response import Response
from rest_framework.decorators import api_view
from discovery import DiscoveryClient
from django.conf import settings

discovery = DiscoveryClient()


# Create your views here.
@api_view(['POST'])
def rec_list(request):
    tags = "".join(request.data['tags'])
    games_list = discovery.query(
        collection_id=settings.DISCOVERY_COLLECTION_ID,
        environment_id=settings.DISCOVERY_ENVIRONMENT_ID,
        natural_language_query=tags)['results']
    results = []
    for game in games_list:
        results.append({"name": game['name'], "summary": game['summary'], "cover": game['cover'],
                        "slug": game['slug']})

    return Response(results)


@api_view(['POST'])
def game_detail(request):
    if request.method == 'POST':
        slug = request.data['slug']
        game = discovery.query(
            collection_id=settings.DISCOVERY_COLLECTION_ID,
            environment_id=settings.DISCOVERY_ENVIRONMENT_ID,
            filter="slug::" + slug)['results'][0]

        return Response(game)
