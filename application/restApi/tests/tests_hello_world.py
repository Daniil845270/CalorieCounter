# #https://mlsaunilag.hashnode.dev/a-practical-approach-to-unit-testing-in-django-rest-framework

# import pytest
# # from django.test import TestCase
# # from ..models import DietStats
# from rest_framework.test import APIClient
# from django.core.exceptions import ValidationError

# @pytest.fixture()  
# def api_client() -> APIClient:  
#     """  
#     Fixture to provide an API client  
#     """  
#     yield APIClient()




# # class SanityCheck(TestCase):
# #     """
# #     the first ever automated test to see if what I did works
# #     """

# #     def test_first_test(self):

# #         DietStats.objects.create(
# #             meal_name="salmon",
# #             meal_type="B", 
# #             protein_per_100g=24.2,
# #             carbohydrates_per_100g=1.0,
# #             fat_per_100g=8.3,
# #             kcal_per_100g=176,
# #             food_item_mass_in_grams=76,
# #         )

# #         salmon = DietStats.objects.get(meal_name="salmon")
# #         self.assertEqual(salmon.meal_type, "B")
# #         self.assertAlmostEqual(salmon.protein_consumed, 18.392, delta=0.001)
# #         self.assertAlmostEqual(salmon.carbohydrates_consumed, 0.76, delta=0.001)
# #         self.assertAlmostEqual(salmon.fat_consumed, 6.308, delta=0.001)
# #         self.assertAlmostEqual(salmon.kcal_consumed, 133.76,  delta=0.001)


