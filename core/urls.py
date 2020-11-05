from rest_framework import routers

from core.views.game import GameViewSet
from core.views.suggestion import SuggestionViewSet
from core.views.favorite import FavoriteViewSet

core_router = routers.SimpleRouter()
core_router.register(r'games', GameViewSet, basename='games')
core_router.register(r'suggestions', SuggestionViewSet, basename='suggestions')
core_router.register(r'favorites', FavoriteViewSet, basename='favorites')
