from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Suggestion


class SuggestionViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['GET'])
    def search(self, request):
        suggestions = Suggestion.objects.filter(
            name__contains=request.query_params.get('search', '')
        )[:5].values_list('name', flat=True)
        return Response([{'label': s, 'value': s} for s in suggestions])
