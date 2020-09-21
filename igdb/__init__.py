import requests
from django.conf import settings


class IGDBClient:
    def __init__(self):
        twitch_oauth_url = f"https://id.twitch.tv/oauth2/token?" \
                           f"client_id={settings.TWITCH_CLIENT_ID}" \
                           f"&client_secret={settings.TWITCH_CLIENT_SECRET}" \
                           f"&grant_type=client_credentials"
        response = requests.post(twitch_oauth_url)
        data = response.json()
        self.access_token = data['access_token']

    def query_top_games(self, total=1000, step=250):
        headers = {"Client-ID": settings.TWITCH_CLIENT_ID, "Authorization": f"Bearer {self.access_token}"}
        games = []
        for i in range(total // step):
            query = f"""fields artworks.*,category,cover.*,genres.name,genres.slug,
            hypes,keywords.name,keywords.slug,name,platforms,player_perspectives.name,
            player_perspectives.slug,rating,rating_count,release_dates.date,screenshots.*,
            similar_games,slug,status,storyline,summary,tags,themes.name,themes.slug,
            total_rating,total_rating_count,url,videos.*,websites.url;
            where platforms = (6, 48, 49, 130) & category = 0 & hypes > 0;
            sort hypes desc;
            limit ${step};
            offset ${i * step};"""
            response = requests.post("https://api.igdb.com/v4/games", data=query, headers=headers)
            games.extend(response.json())
        return games
