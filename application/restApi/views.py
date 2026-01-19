from restApi.models import DietStats
from restApi.serializers import DietStatsSerializer, AverageKcalSerializer
from rest_framework import mixins
from rest_framework import generics
import datetime
from django.db.models import Avg, Sum
from rest_framework.views import APIView
from rest_framework.response import Response


class DietStatsView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = DietStats.objects.all()
    serializer_class = DietStatsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs) 


# retrieves all of the objects from the database
class SimpleAllObjectRetrievalView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = DietStats.objects.all()
    serializer_class = DietStatsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# retrieves a single object with a specified id
class SimpleSingleObjectRetrievalView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = DietStats.objects.all()
    serializer_class = DietStatsSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# this code returns the macronutrient and kcal summary of the food eaten over the past year
class PastYearStatisticsView(APIView):
    """
    Get the averages of macros and kcal from the entries of the past year and send them to the client
    """

    def get(self, request, format=None):
        last_year = datetime.date.today() - datetime.timedelta(days=360)
        date_today = datetime.date.today()

        year_average = DietTracking.get_averages_over_time(last_year, date_today)
        
        serialised = AverageKcalSerializer(year_average)

        return Response(serialised.data)
    
class PastMonthStatisticsView(APIView):
    """
    Get the averages of macros and kcal from the entries of the past year and send them to the client
    """

    def get(self, request, format=None):
        last_year = datetime.date.today() - datetime.timedelta(days=30)
        date_today = datetime.date.today()

        year_average = DietTracking.get_averages_over_time(last_year, date_today)
        
        serialised = AverageKcalSerializer(year_average)

        return Response(serialised.data)
    
# there must be a better way to do this, than repeating yourself. 
# Maybe create a separate form and extract the query parameters form the url of the query?
class PastWeekStatisticsView(APIView):
    """
    Get the averages of macros and kcal from the entries of the past year and send them to the client
    """

    def get(self, request, format=None):
        last_year = datetime.date.today() - datetime.timedelta(days=7)
        date_today = datetime.date.today()

        year_average = DietTracking.get_averages_over_time(last_year, date_today)
        
        serialised = AverageKcalSerializer(year_average)

        return Response(serialised.data)

# this code returns the food items eaten over the past year
class PastYearObjectRetrievalView(mixins.ListModelMixin, generics.GenericAPIView):
    
    def get_queryset(self):
        date_exactly_last_year = datetime.date.today() - datetime.timedelta(days=360)
        date_today = datetime.date.today()
        return DietStats.objects.filter(
            entry_date__gte=date_exactly_last_year,
            entry_date__lte=date_today)
    
    serializer_class = DietStatsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DietTracking():

    def get_averages_over_time(start_date, end_date):

        result = DietStats.objects.filter( 
            entry_date__gte=start_date,
            entry_date__lte=end_date).aggregate(
                Avg("kcal_consumed"),
                Avg("protein_consumed"),
                Avg("fat_consumed"),
                Avg("carbohydrates_consumed"))
        
        return result
    
    # date must contain year, month and day
    def get_cumulative_stats_per_day(date):

        result = DietStats.objects.filter(
            entry_date=date
            ).aggregate(
                total_protein=Sum("protein_consumed"),
                total_fat=Sum("fat_consumed"),
                total_carbohydrates=Sum("carbohydrates_consumed"),
                total_kcal=Sum("kcal_consumed"))
        return result
    
    
    def get_daily_progression(this_day, another_day):

        this_day_cumulative = DietStats.objects.filter(
            entry_date=this_day
            ).aggregate(
                total_protein=Sum("protein_consumed"),
                total_fat=Sum("fat_consumed"),
                total_carbohydrates=Sum("carbohydrates_consumed"),
                total_kcal=Sum("kcal_consumed"))
        
        another_day_cumulative = DietStats.objects.filter(
            entry_date=another_day
            ).aggregate(
                total_protein=Sum("protein_consumed"),
                total_fat=Sum("fat_consumed"),
                total_carbohydrates=Sum("carbohydrates_consumed"),
                total_kcal=Sum("kcal_consumed"))
        
        progression = {}
        
        for key in this_day_cumulative.keys():
            progression[key] = this_day_cumulative[key] - another_day_cumulative[key]

        return progression
    
    # def get_weekly_progression -> to implement

    
    
