import io
import json

from django.conf import settings

from discovery import DiscoveryClient
from igdb import IGDBClient


def load_games_into_discovery(total=10, step_size=10):
    igdb = IGDBClient()
    discovery = DiscoveryClient()

    discovery.setup(environment_name=settings.DISCOVERY_ENVIRONMENT, collection_name=settings.DISCOVERY_COLLECTION)
    games = igdb.query_top_games(total=total, step=step_size)
    for game in games:
        with io.StringIO() as file:
            json.dump(game, file)
            file.seek(0)
            discovery.add_document(file=file, filename=f"{game['slug']}.json")
            print(f"Processed {game['name']}")
