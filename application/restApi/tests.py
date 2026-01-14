import datetime

from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from .models import DietStats


class DoesItEvenWorkTest(TestCase):
    """
    the first ever automated test to see if what I did works
    """
    def setUp(self):
        DietStats.objects.create(
            name="salmon",
            meal_type="B", 
            protein_per_100g="24.2",
            carbohydrates_per_100g="1.0",
            fat_per_100g="8.3",
            kcal_per_100g="176",
            food_item_mass_in_grams="76",
        )


    def test_first_test(self):
        salmon = DietStats.objects.get(name="salmon")
        self.assertEqual(salmon.meal_type, "B")
        self.assertEqual(salmon.protein_per_100g, Decimal("24.2"))
