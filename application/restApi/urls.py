"""
Write the basic view and then come here to set the endpoints
"""

from django.urls import path
from restApi import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("diet/", views.DietStatsView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
