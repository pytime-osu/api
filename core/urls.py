from rest_framework import routers

from core.views.game import GameViewSet

core_router = routers.SimpleRouter()
core_router.register(r'games', GameViewSet, basename='games')
