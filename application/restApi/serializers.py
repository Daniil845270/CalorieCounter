from rest_framework import serializers
from .models import DietStats
import datetime

class DietStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietStats
        fields = '__all__'

    # do I need a validator for a choice field? 
    def validate(self, data):
        
        if (data['protein_per_100g'] < 0 or 
            data['carbohydrates_per_100g'] < 0 or 
            data['fat_per_100g'] < 0 or
            data['food_item_mass_in_grams'] < 0 or
            data['kcal_per_100g'] < 0):
            raise serializers.ValidationError('nutrition values can not be negative')
        
        if (data['protein_per_100g'] > 100 or 
            data['carbohydrates_per_100g'] > 100 or 
            data['fat_per_100g'] > 100):
            raise serializers.ValidationError('100 grams of food can not have more than a 100g of a macronutrient')
        
        # what would be cool to implement is "click the submit button the second time to confirm you are absolutely 
        # sure you want to submit this data", like when creating a weak password in fedora account
        if (data['food_item_mass_in_grams'] > 5000 or 
            data['kcal_per_100g'] > 900):
            raise serializers.ValidationError('The food mass or kcal value is too big.')
        
        if data['protein_per_100g'] + data['carbohydrates_per_100g'] + data['fat_per_100g'] > 100:
            raise serializers.ValidationError("Sum of macronutrients per 100g can not 100g")
        
        """
        when I will start implementing the user class, I will need to adapt the code to support different timezones
        """
        if data['entry_date'] - datetime.date.today() > datetime.timedelta(days=6):
            raise serializers.ValidationError("You can not enter items more than a week in a future")
        
        """
        Validating Free-form Unicode Text appears to be too big of a topic for the purpose of the project at the current state. 
        Therefore, for security reasons, I'll just restrict the valid input to the a set of allowed characters
        """ 
        submitted_name = " ".join(data['meal_name'].strip().split())
        if submitted_name == '':
            raise serializers.ValidationError("Item must have a name")
        
        allowlist_string = ("abcdefghijklmnopqrstuvwxyz"
                            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            "1234567890 ") #letter, numbers and a whitespace
        
        for char in submitted_name:
            if char not in allowlist_string:
                raise serializers.ValidationError("Food item contains illegal characters. Use only letters and numbers")
            
        if len(submitted_name) > 100:
            raise serializers.ValidationError("Item name is too long")
            
        data['meal_name'] = submitted_name
  
        return data


# this serialiser doesn't really need validation since I'm not deserialising data
class AverageKcalSerializer(serializers.Serializer):
    protein_consumed__avg = serializers.FloatField(read_only=True)
    carbohydrates_consumed__avg = serializers.FloatField(read_only=True)
    fat_consumed__avg = serializers.FloatField(read_only=True)
    kcal_consumed__avg = serializers.FloatField(read_only=True) 

