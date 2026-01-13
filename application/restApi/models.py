# okay, so the goal for today is to create a simple database model, and remember how to test whether it doesn't have any bugs
# what do I want the end user to include into the table?
    # the category of a meal (breakfast, lunch, dinner, snack, other)
    # an estimate of the nutritious content (protein, sugars + carbohydrates, fat + saturates, energy in kcal, (salt?))
    # date of when each entry was added
    # a coupe of columns where some values would be calculated from the others
        # cumulative energy/protein/sugar/fat intake for that day
        # average daily intake for a week/month/year
            # since I am adding a breakfast/lunch/dinner categories, maybe I can also make the statistics for 
            # the food intake statistics for particular periods of times?
# maybe it would also be useful to add a comment section


# I will need to create a user model, which
    # has a many to one relationship with the dietary information table, where 1 user can have more than one table (why?)
# I will need to create a user model, where 
    # 
# when I will create a user interface, it may be a good idea to create a feature, where, for example, if you

# when done, think about form validation, and how to test all of this


# what I actually haven't thought about is that when I write the calory information of a product, I also need to write, how much 
# of it was consumed -> also need to calculate the product of calories * mass of the food item

from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class DietStats(models.Model):

    # This part of the table consists of the values the user inputs

    MEAL_TYPE_CHOICES = {
        "B": "Breakfast",
        "L": "Lunch",
        "D": "Dinner",
        "S": "Snack",
        "O": "Other",
    }

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

    # this decimal thing looks too excessive and ugly, consider getting rid of it
    protein = models.DecimalField( 
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(Decimal("0.0")),
                    MaxValueValidator(Decimal("100.0")),],
    )
    carbohydrates = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        validators=[MinValueValidator(Decimal("0.0")),
                    MaxValueValidator(Decimal("100.0")),],
    )
    fat = models.DecimalField(
        max_digit=4,
        decimal_places=1,
        validators=[MinValueValidator(Decimal("0.0")),
                    MaxValueValidator(Decimal("100.0")),],
    )
    # in kcal per 100g, should here be an upper limit?
    energy = models.PositiveIntegerField(
        validators=[MinValueValidator(Decimal("0.0"))],
    ) 
    
    # consider adding these 2 later, when the base stuff is working
    # sugars = models.DecimalField(
    #     max_digits=4,
    #     decimal_places=1,
    #     validators=[MinValueValidator(Decimal("0.0")),
    #                 MaxValueValidator(Decimal("100.0")),],
    # )
    # saturates = models.DecimalField(
    #     max_digits=4,
    #     decimal_places=1,
    #     blank=True,
    #     validators=[MinValueValidator(Decimal("0.0")),
    #                 MaxValueValidator(Decimal("100.0")),],
    # )

    # this part of the table consists of the values that are calculated based on the user input


# figure this out later
# class User(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)