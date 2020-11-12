from functools import reduce

from django.db.models import Q, Count
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Cover


class CoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        fields = '__all__'


class CoverViewSet(viewsets.ModelViewSet):
    queryset = Cover.objects.all()
    serializer_class = CoverSerializer
    filterset_fields = ['game']

    @action(detail=False, methods=['POST'])
    def match(self, request):
        games = request.data.get('games', [])
        search = request.data.get('search', [])
        tag_query = reduce(lambda q, t: q | Q(tag__contains=t.lower()), search, Q())
        tags = Cover.objects.filter(game__in=games).filter(tag_query)
        scores = tags.values('game', 'image', 'size').annotate(score=Count('tag')).order_by('-score', '-size')
        return Response(data=scores)
