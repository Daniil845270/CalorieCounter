from django.urls import path, include
from restApi import views
from rest_framework.urlpatterns import format_suffix_patterns
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path("diet/", views.DietStatsView.as_view()),
    path("descriptionsLC/", views.LCFoodDescriptionView.as_view()),
    path("entriesLC/", views.LCFoodEntryView.as_view()),
    path("descriptionsRUD/<int:pk>/", views.RUDFoodDescriptionView.as_view()),
    path("entriesRUD/<int:pk>/", views.RUDFoodEntryView.as_view()),
    path('silk/', include('silk.urls', namespace='silk')),
]

urlpatterns = format_suffix_patterns(urlpatterns)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)