from rest_framework import serializers
from .models import DietStats, FoodDescriptionModel, FoodEntryModel
import datetime

# for the validators of the new models, I reused the same logic for the old validators
# good enough for now, but later audit the code and improve upon it
class FoodDescriptionSerializer(serializers.ModelSerializer):
    Item_name = serializers.CharField(source="item_name", max_length=100)
    Protein_per_100g = serializers.FloatField(source="prtn100")
    Carbohydrate_per_100g = serializers.FloatField(source="carb100")
    Fat_per_100g = serializers.FloatField(source="fat100")
    Kcal_per_100g = serializers.FloatField(source="kcal100")

    
    class Meta:
        model = FoodDescriptionModel
        fields = [
            'id',
            "description_owner",
            "Item_name",
            "Protein_per_100g",
            "Carbohydrate_per_100g",
            "Fat_per_100g",
            "Kcal_per_100g",
            "created_at",
            "first_created_date",
            "last_updated_date"
        ]

    def validate(self, data):
        
        if (data['prtn100'] < 0 or 
            data['carb100'] < 0 or 
            data['fat100'] < 0 or
            data['kcal100'] < 0):
            raise serializers.ValidationError('nutrition values can not be negative')
        
        if (data['prtn100'] > 100 or 
            data['carb100'] > 100 or 
            data['fat100'] > 100):
            raise serializers.ValidationError('100 grams of food can not have more than a 100g of a macronutrient')
        
        # what would be cool to implement is "click the submit button the second time to confirm you are absolutely 
        # sure you want to submit this data", like when creating a weak password in fedora account
        if (data['kcal100'] > 900):
            raise serializers.ValidationError('kcal value is too big.')
        
        if data['prtn100'] + data['carb100'] + data['fat100'] > 100:
            raise serializers.ValidationError("Sum of macronutrients per 100g can not 100g")
        
        """
        when I will start implementing the user class, I will need to adapt the code to support different timezones
        """
        if data['created_at'] - datetime.date.today() > datetime.timedelta(days=6):
            raise serializers.ValidationError("You can not enter items more than a week in a future")
        
        """
        Validating Free-form Unicode Text appears to be too big of a topic for the purpose of the project at the current state. 
        Therefore, for security reasons, I'll just restrict the valid input to the a set of allowed characters
        """ 
        submitted_name = " ".join(data['item_name'].strip().split())
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
            
        data['item_name'] = submitted_name
  
        return data
    
class FoodEntrySerializer(serializers.ModelSerializer):
    entries = FoodDescriptionSerializer()

    class Meta:
        model = FoodEntryModel
        fields = '__all__'
    
    def validate(self, data):
        if data['item_mass'] < 0:
            raise serializers.ValidationError('nutrition values can not be negative')
        
        if data['food_item_mass_in_grams'] > 5000:
            raise serializers.ValidationError('The food mass value is too big.')



class DietStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietStats
        fields = '__all__'

    # do I need a validator for a choice field? 
    def validate(self, data):
        
        if (data['protein_per_100g'] < 0 or 
            data['sugar_per_100g'] < 0 or 
            data['fat_per_100g'] < 0 or
            data['food_item_mass_in_grams'] < 0 or
            data['kcal_per_100g'] < 0):
            raise serializers.ValidationError('nutrition values can not be negative')
        
        if (data['protein_per_100g'] > 100 or 
            data['sugar_per_100g'] > 100 or 
            data['fat_per_100g'] > 100):
            raise serializers.ValidationError('100 grams of food can not have more than a 100g of a macronutrient')
        
        # what would be cool to implement is "click the submit button the second time to confirm you are absolutely 
        # sure you want to submit this data", like when creating a weak password in fedora account
        if (data['food_item_mass_in_grams'] > 5000 or 
            data['kcal_per_100g'] > 900):
            raise serializers.ValidationError('The food mass or kcal value is too big.')
        
        if data['protein_per_100g'] + data['sugar_per_100g'] + data['fat_per_100g'] > 100:
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
    sugar_consumed__avg = serializers.FloatField(read_only=True)
    fat_consumed__avg = serializers.FloatField(read_only=True)
    kcal_consumed__avg = serializers.FloatField(read_only=True) 

