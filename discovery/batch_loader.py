import io
import json

from django.conf import settings

from core.models import Suggestion
from discovery import DiscoveryClient
from igdb import IGDBClient


def load_games_into_discovery(total=10, step_size=10):
    igdb = IGDBClient()
    discovery = DiscoveryClient()
    Suggestion.objects.all().delete()
    suggestions = set()
    discovery.setup(environment_name=settings.DISCOVERY_ENVIRONMENT, collection_name=settings.DISCOVERY_COLLECTION)
    games = igdb.query_top_games(total=total, step=step_size)
    for game in games:
        if 'keywords' in game:
            suggestions.update([k['name'].lower() for k in game['keywords']])
        if 'genres' in game:
            suggestions.update([g['name'].lower() for g in game['genres']])
        if 'player_perspectives' in game:
            suggestions.update([p['name'].lower() for p in game['player_perspectives']])
        if 'themes' in game:
            suggestions.update([t['name'].lower() for t in game['themes']])
        with io.StringIO() as file:
            json.dump(game, file)
            file.seek(0)
            discovery.add_document(file=file, filename=f"{game['slug']}.json")
            print(f"Processed {game['name']}. Suggestion count: {len(suggestions)}.")
    for s in suggestions:
        Suggestion.objects.create(name=s)
    print(discovery.environment)
    print(discovery.collection)
