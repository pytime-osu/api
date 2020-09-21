# api
Django API

## Using the batch loader
Get a Twitch Client ID and Secret from here: https://dev.twitch.tv/
View this document for more instructions: https://api-docs.igdb.com/?javascript#breaking-changes

Add these environmental variables to your shell:
* `DISCOVERY_API_KEY`: API Key from IBM Discovery
* `DISCOVERY_SERVICE_URL`: Service URL from IBM Discovery
* `TWITCH_CLIENT_ID`: Client ID from Twitch Developers
* `TWITCH_CLIENT_ID`: Client Secret from Twitch Developers

Once you have done that, you can run the batch loader:
```
from discovery.batch_loader import load_games_into_discovery
load_games_into_discovery(total=10, step_size=10)
```

The total is the total amount of games to fetch (so don't go over 1,000), and the step size is how may to query in one IGDB call.
There is no limit, but keep it small otherwise the response from the IGDB API will take a long time to download.
