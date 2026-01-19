from rest_framework import serializers
from .models import DietStats

# the future validation will be implemented here (for example, that the weight of macronutrients per grams must be within 0 and 100)

# consider looking into modifying the create and update methods to figure out the validation
# also consider using a serializers. HyperlinkedModelSerializer instead of a model one 
class DietStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietStats
        fields = '__all__'

    def validate_protein_consumed(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('The protein content value must be between 0 and a 100')
        return value
    
    # come back here when the basic functionality of the application is done
    # also figure out if I need an object-level validation 

class AverageKcalSerializer(serializers.Serializer):
    protein_consumed__avg = serializers.FloatField(read_only=True)
    carbohydrates_consumed__avg = serializers.FloatField(read_only=True)
    fat_consumed__avg = serializers.FloatField(read_only=True)
    kcal_consumed__avg = serializers.FloatField(read_only=True) 

