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
    Suggestion.objects.all().delete()
    suggestions = set()
    discovery.setup(environment_name=settings.DISCOVERY_ENVIRONMENT, collection_name=settings.DISCOVERY_COLLECTION)
    shows = tmdb.query_top_shows(total)
    for show in shows[:total]:
        if 'genres' in show:
            suggestions.update([g['name'].lower() for g in show['genres']])
        if 'created_by' in show:
            suggestions.update([c['name'].lower() for c in show['created_by']])
        if 'networks' in show:
            suggestions.update([n['name'].lower() for n in show['networks']])
        if 'production_companies' in show:
            suggestions.update([p['name'].lower() for p in show['production_companies']])
        with io.StringIO() as file:
            json.dump(show, file)
            file.seek(0)
            discovery.add_document(file=file, filename=f"{show['name']}.json")
            print(f"Processed {show['name']}. Suggestion count: {len(suggestions)}.")
    for s in suggestions:
        Suggestion.objects.create(name=s)
    print(discovery.environment)
    print(discovery.collection)