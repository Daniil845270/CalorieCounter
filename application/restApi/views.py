from restApi.models import DietStats, FoodDescriptionModel, FoodEntryModel
from restApi.serializers import DietStatsSerializer, FoodDescriptionSerializer, FoodEntrySerializer, SummaryViewSerializer, FullDataFoodEntriesSerializer
from rest_framework import mixins
from rest_framework import generics
import datetime
from django.db.models import Avg, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class LCFoodDescriptionView(generics.ListCreateAPIView):
    queryset = FoodDescriptionModel.objects.all()
    serializer_class = FoodDescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(description_owner=user)
    

class RUDFoodDescriptionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodDescriptionModel.objects.all()
    serializer_class = FoodDescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(description_owner=user)

class LCFoodEntryView(generics.ListCreateAPIView):
    queryset = FoodEntryModel.objects.all()
    serializer_class = FoodEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(entry_owner=user)
    
class RUDFoodEntryView(generics.ListCreateAPIView):
    queryset = FoodEntryModel.objects.all()
    serializer_class = FoodEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(entry_owner=user)
    


"""
SummaryView is designed give a snapshot of the statistics for a period of time,
be that a day(s), week(s), month(s), year(s)

the accepted request should be in a format of GET /analytics/summary?start=YYYY-MM-DD&end=YYYY-MM-DD 
(also including the time, since I moved to datetime)

may also implement the presents (/analytics/summary?preset=last_7_days)

the return object should contain the summaries of of energy and macronutrients in the form of mean, median and mode
    more specifically, I need to return the statistics of the energy and macros per 100 grams AND for the actual amount of 
    food items consumed (values per 100 / grams consumed)

"""
class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        data = request.query_params

        if 'start' in data and 'end' in data:
            start, end = data['start'], data['end']
            serializer = SummaryViewSerializer(data={'start': start, 'end': end})
            if not serializer.is_valid():
                return Response(serializer.errors)
            user = self.request.user
            queryset = FoodEntryModel.objects.filter(
                entry_owner=user
                ).filter(
                    consumed_date__range=(start, end)
                    )
            serializer = FullDataFoodEntriesSerializer(queryset, many=True)

            # now that I have a queryset, I can iterate over the instances, extract the data, make the calculations, and return the summary!
            
            return Response(serializer.data)

        elif 'preset' in data:
            return Response({"hello": "contains preset"})
        
        return Response(status.HTTP_400_BAD_REQUEST) # search online on how to return bad request error

class TimeseriesView(APIView):

    def get(self, request, format=None):
        pass

class BreakdownView(APIView):

    def get(self, request, format=None):
        pass

class FlagsView(APIView):

    def get(self, request, format=None):
        pass

"""
and I have just realised that instead of this I could (and in fact should have used from the beginning) 
a RetrieveUpdateDestroyAPIView, CreateAPIView and ListAPIView that actually does more than I wanted
"""

class DietStatsView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = DietStats.objects.all()
    serializer_class = DietStatsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs) 
