from django.db import models
import datetime
# from django.core.validators import MaxValueValidator, MinValueValidator

class DietStats(models.Model):
    """
    This part of the table consists of the values the user inputs
    """

    MEAL_TYPE_CHOICES = {
        "B": "Breakfast",
        "L": "Lunch",
        "D": "Dinner",
        "S": "Snack",
        "O": "Other",
    }

    meal_name = models.CharField(max_length=100)

    # TEST CASE: when the database is working, figure out how to add per user date 
    # https://docs.djangoproject.com/en/6.0/topics/i18n/timezones/
    entry_date = models.DateField( 
        default=datetime.date.today,
    )

    meal_type = models.CharField( 
        max_length=1,
        choices=MEAL_TYPE_CHOICES,
        )
    
    # given that the protein, sugar and fat content is calculated out of a 100g, then the highest possible value that could be 
    # there is 100.0 -> TEST CASE
    # one problem with DecimalField is that all of the values here must be non-negative -> TEST CASE

    protein_per_100g = models.FloatField()
    carbohydrates_per_100g = models.FloatField()
    fat_per_100g = models.FloatField()
    kcal_per_100g = models.FloatField()
    food_item_mass_in_grams = models.PositiveIntegerField() 

    """
    This part of the table consists of the values that are calculated form the user input 
    """

    protein_consumed = models.GeneratedField(
        expression= (models.F("protein_per_100g") * 
                     models.F("food_item_mass_in_grams")) / 
                     100,
        output_field=models.FloatField(),
        db_persist=True
    )

    carbohydrates_consumed = models.GeneratedField(
        expression= (models.F("carbohydrates_per_100g") * 
                     models.F("food_item_mass_in_grams")) / 
                     100,
        output_field=models.FloatField(),
        db_persist=True
    )

    fat_consumed = models.GeneratedField(
        expression= (models.F("fat_per_100g") * 
                     models.F("food_item_mass_in_grams")) / 
                     100,
        output_field=models.FloatField(),
        db_persist=True
    )

    kcal_consumed = models.GeneratedField(
        expression= (models.F("kcal_per_100g") * 
                     models.F("food_item_mass_in_grams")) / 
                     100,
        output_field=models.FloatField(),
        db_persist=True
    )
