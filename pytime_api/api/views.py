from rest_framework import viewsets, permissions
from discovery import DiscoveryClient
from django.conf import settings

# Create your views here.
class GameViewSet(viewsets.ModelViewSet):
    discovery = DiscoveryClient()
    discovery.setup(environment_name=settings.DISCOVERY_ENVIRONMENT, collection_name=settings.DISCOVERY_COLLECTION)