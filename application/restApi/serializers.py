from rest_framework import serializers
from .models import DietStats

# consider looking into modifying the create and update methods to figure out the validation
# also consider using a serializers. HyperlinkedModelSerializer instead of a model one 
class DietStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietStats
        fields = '__all__'