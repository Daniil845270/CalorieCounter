from restApi.models import DietStats
from restApi.serializers import DietStatsSerializer
from rest_framework import mixins
from rest_framework import generics

class DietStatsView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = DietStats.objects.all()
    serializer_class = DietStatsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs) 