from rest_framework.response import Response
from rest_framework.decorators import api_view
from discovery import DiscoveryClient
import json

collection_id = "6b937524-1cca-42bd-88a4-3d6871db5ab5"
environment_id = "9ee59277-ba86-4516-b46c-81f2003c3d9a"


# Create your views here.
@api_view(['POST'])
def rec_list(request):
    if request.method == 'POST':
        tag = request.data['tag']
        discovery = DiscoveryClient()
        games_list = discovery.query(
            collection_id=collection_id,
            environment_id=environment_id,
            natural_language_query=tag).get_result()['results']
        results = []
        for game in games_list:
            results.append({"name": game['name'], "summary": game['summary'], "cover_url": game['cover']['url']})

        return Response(results)