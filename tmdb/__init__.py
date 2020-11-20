import tmdbsimple as tmdb
from django.conf import settings


class TMDBClient:
    def __init__(self):
        tmdb.API_KEY = settings.TMDB_API_KEY

    def query_top_shows(self, total=1000):
        tv = tmdb.TV()
        pop_shows = []
        results = []

        # 20 results per page in API
        for i in range(1, total // 20 + 1):
            pop_shows += tv.popular(page=i)['results']

        for show in pop_shows:
            temp = tmdb.TV(show['id'])
            results.append(temp.info())

        return results
