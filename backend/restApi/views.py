from restApi.models import DietStats, FoodDescriptionModel, FoodEntryModel
from restApi.serializers import (DietStatsSerializer, 
                                 FoodDescriptionSerializer, 
                                 FoodEntrySerializer, 
                                 SummaryViewSerializer, 
                                 FullDataFoodEntriesSerializer, 
                                 UserSerializer)
from rest_framework import mixins, generics
from django.db.models import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from restApi.service import CalculateSummary
from django.contrib.auth.models import User
 

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

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

the accepted request must be in a format of GET /analytics/summary?start=YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]&end=YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]

Write the rest of documentation for this function

"""
class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        data = request.query_params

        if 'start' in data and 'end' in data:
            start, end = data['start'], data['end']
            serializer = SummaryViewSerializer(data={'start': start, 'end': end})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = self.request.user
            queryset = FoodEntryModel.objects.filter(
                entry_owner=user
                ).filter(
                    consumed_date__range=(start, end)
                    )
            serializer = FullDataFoodEntriesSerializer(queryset, many=True)
            data: list[QuerySet] = serializer.data 
            # return  Response(data)
            statisticsPerDay, statisticsDailyDifference = CalculateSummary(data)
            return Response([statisticsPerDay, statisticsDailyDifference])

        elif 'preset' in data:
            return Response({"hello": "contains preset"})
        
        return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

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
