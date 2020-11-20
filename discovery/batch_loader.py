import io
import json

from django.conf import settings

from core.models import Suggestion
from discovery import DiscoveryClient
from tmdb import TMDBClient


# Keeping old suggestion stuff for now so it can be updated later
def load_shows(total=20):
    tmdb = TMDBClient()
    discovery = DiscoveryClient()
    # Suggestion.objects.all().delete()
    # suggestions = set()
    discovery.setup(environment_name=settings.DISCOVERY_ENVIRONMENT, collection_name=settings.DISCOVERY_COLLECTION)
    shows = tmdb.query_top_shows(total)
    for show in shows[:total]:
        with io.StringIO() as file:
            json.dump(show, file)
            file.seek(0)
            discovery.add_document(file=file, filename=f"{show['name']}.json")
    print(discovery.environment)
    print(discovery.collection)

    # games = igdb.query_top_games(total=10)
    # for game in games:
    #     if 'keywords' in game:
    #         suggestions.update([k['name'].lower() for k in game['keywords']])
    #     if 'genres' in game:
    #         suggestions.update([g['name'].lower() for g in game['genres']])
    #     if 'player_perspectives' in game:
    #         suggestions.update([p['name'].lower() for p in game['player_perspectives']])
    #     if 'themes' in game:
    #         suggestions.update([t['name'].lower() for t in game['themes']])
    #     with io.StringIO() as file:
    #         json.dump(game, file)
    #         file.seek(0)
    #         discovery.add_document(file=file, filename=f"{game['slug']}.json")
    #         print(f"Processed {game['name']}. Suggestion count: {len(suggestions)}.")
    # for s in suggestions:
    #     Suggestion.objects.create(name=s)
    # print(discovery.environment)
    # print(discovery.collection)
