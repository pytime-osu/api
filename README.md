# api
Django API

## Using the batch loader
Get a TMDB API Key from here: https://www.themoviedb.org/
View this document for more instructions: https://www.themoviedb.org/documentation/api

Add these environmental variables to your shell:
* `DISCOVERY_API_KEY`: API Key from IBM Discovery
* `DISCOVERY_SERVICE_URL`: Service URL from IBM Discovery
* `TMDB_API_KEY`: API Key from TMDB

Once you have done that, you can run the batch loader:
```
from discovery.batch_loader import load_shows
load_shows(total=20)
```

The total is the total amount of shows to fetch (so don't go over 1,000) and should be inputted in multiples of 20.
Expect 5-10 minutes for total=1000.
