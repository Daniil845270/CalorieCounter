import datetime

from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from .models import DietStats


class SanityCheck(TestCase):
    """
    the first ever automated test to see if what I did works
    """

    def test_first_test(self):

        DietStats.objects.create(
            meal_name="salmon",
            meal_type="B", 
            protein_per_100g=24.2,
            carbohydrates_per_100g=1.0,
            fat_per_100g=8.3,
            kcal_per_100g=176,
            food_item_mass_in_grams=76,
        )

        salmon = DietStats.objects.get(meal_name="salmon")
        self.assertEqual(salmon.meal_type, "B")
        self.assertAlmostEqual(salmon.protein_consumed, 18.392, delta=0.001)
        self.assertAlmostEqual(salmon.carbohydrates_consumed, 0.76, delta=0.001)
        self.assertAlmostEqual(salmon.fat_consumed, 6.308, delta=0.001)
        self.assertAlmostEqual(salmon.kcal_consumed, 133.76,  delta=0.001)

    # def test_negative_numbers(self):
        
    #     negative = DietStats.objects.create(
    #         meal_name="negative protein",
    #         meal_type="B", 
    #         protein_per_100g=-24.2,
    #         carbohydrates_per_100g=1.0,
    #         fat_per_100g=8.3,
    #         kcal_per_100g=176,
    #         food_item_mass_in_grams=76,
    #     )

    #     negative.

    #     # try:
    #     #     negative.save()
    #     # except:
    #     #     self.assertRaises(ValidationError, validate_percent, 1000)


    #     # salmon = DietStats.objects.get(meal_name="negative protein")
    #     # self.assertEqual(salmon.meal_type, "B")
    #     # self.assertAlmostEqual(salmon.protein_consumed, -18.392, delta=0.001)
    #     # self.assertAlmostEqual(salmon.carbohydrates_consumed, 0.76, delta=0.001)
    #     # self.assertAlmostEqual(salmon.fat_consumed, 6.308, delta=0.001)
    #     # self.assertAlmostEqual(salmon.kcal_consumed, 133.76,  delta=0.001)