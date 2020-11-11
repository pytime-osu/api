from rest_framework import viewsets, serializers

from core.models import Cover


class CoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        fields = '__all__'


class CoverViewSet(viewsets.ModelViewSet):
    queryset = Cover.objects.all()
    serializer_class = CoverSerializer
    filterset_fields = ['game']
