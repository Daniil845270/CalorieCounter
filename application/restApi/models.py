"""
Plan or summary of what I actually intend to implement

you as a user your look at the back of a food product packaging, and enter 
- proteins, fat, sugars and kcal for 100g of the product, and the weight in grams of the product that you have eaten
- then the table calculates the actual macronutrients and energy content of the food you eaten, based on the calculations 
- also, the table may have a functionality of calculating summary of the statistics per day/week/month/year, or by the 
    time period that you request (but that will come later)
"""


"""
I will need to create a user model, which
    has a many to one relationship with the dietary information table, where 1 user can have more than one table (why?)

when done, think about form validation, and how to test all of this
"""

from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

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

    name = models.CharField(max_length=100)

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

    protein_per_100g = models.FloatField( 
        validators=[MinValueValidator(0),
                    MaxValueValidator(100),],
    )
    carbohydrates_per_100g = models.FloatField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100),],
    )
    fat_per_100g = models.FloatField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100),],
    )
    kcal_per_100g = models.FloatField(
        validators=[MinValueValidator(0),],
    )
    food_item_mass_in_grams = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
    ) 

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
