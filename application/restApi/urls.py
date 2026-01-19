from django.urls import path
from restApi import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("diet/", views.DietStatsView.as_view()),
    path("diet/simple/", views.SimpleAllObjectRetrievalView.as_view()),
    path("diet/simple/<int:pk>/", views.SimpleSingleObjectRetrievalView.as_view()),
    path("diet/year/", views.PastYearObjectRetrievalView.as_view()),
    path("diet/stats/", views.PastYearStatisticsView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)