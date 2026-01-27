from django.db import models
import datetime
from django.contrib.auth.models import User

class FoodDescriptionModel(models.Model):
    description_owner = models.ForeignKey(User, 
                              related_name="food_descriptions", 
                              on_delete=models.CASCADE
                              )
    item_name = models.CharField(max_length=100)
    prtn100 = models.FloatField()
    carb100 = models.FloatField()
    fat100 = models.FloatField()
    kcal100 = models.FloatField()
    created_at = models.DateTimeField( 
        default=datetime.datetime.today,
    )
    first_created_date = models.DateTimeField(
        auto_now_add=True,
    )
    last_updated_date = models.DateTimeField(
        auto_now=True,
    )
    # this feature will be cool to add in the future
    # image = models. ImageField(upload_to="images/FoodDescription", blank=True, null=True)

    def __str__ (self):
        return f"A description for {self.item_name} made by {self.description_owner.username}"
    
class FoodEntryModel(models.Model):

    description = models.ForeignKey(FoodDescriptionModel, 
                              related_name="entries", 
                              on_delete=models.CASCADE
                              )
    entry_owner = models.ForeignKey(User, 
                              related_name="food_entries", 
                              on_delete=models.CASCADE
                              )
    item_type = models.CharField( 
        max_length=1,
        choices={
            "B": "Breakfast",
            "L": "Lunch",
            "D": "Dinner",
            "S": "Snack",
            "O": "Other",
        },
    )
    item_mass = models.FloatField() 
    consumed_date = models.DateTimeField( 
        default=datetime.datetime.today,
    )
    # first_created_date = models.DateTimeField(
    #     auto_now_add=True,
    # )
    # last_updated_date = models.DateTimeField(
    #     auto_now=True,
    # )

    def __str__ (self):
        return f"An entry record of {self.description.item_name} made by {self.entry_owner.username} on {self.consumed_date}"

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
    sugar_per_100g = models.FloatField()
    fat_per_100g = models.FloatField()
    kcal_per_100g = models.FloatField()
    food_item_mass_in_grams = models.FloatField() 

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

    sugar_consumed = models.GeneratedField(
        expression= (models.F("sugar_per_100g") * 
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
