from discovery import DiscoveryClient
from django.conf import settings
import requests
import json

collection_id = "6b937524-1cca-42bd-88a4-3d6871db5ab5"
environment_id = "9ee59277-ba86-4516-b46c-81f2003c3d9a"

discovery = DiscoveryClient()
games_list = discovery.query(collection_id=collection_id, environment_id=environment_id, natural_language_query="horses").get_result()['results']
for game in games_list:
    print(game['name'])
    print(game['cover']['url'])
    print(game['summary'])

