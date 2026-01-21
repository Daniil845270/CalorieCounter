import pytest
from datetime import date
from restApi.models import DietStats
from rest_framework.test import APIClient

@pytest.fixture()  
def api_client() -> APIClient:  
    """  
    Fixture to provide an API client  
    """  
    yield APIClient()

@pytest.fixture
def project_payload_standard() -> dict: # uses the user fixture
    return { 
        "meal_name": "standard",
        "entry_date": "2022-05-07",
        "meal_type": "D",
        "protein_per_100g": 1.7,
        "carbohydrates_per_100g": 20.1,
        "fat_per_100g": 0.7,
        "kcal_per_100g": 90.0,
        "food_item_mass_in_grams": 260
    }

@pytest.fixture
def project_payload_alternative() -> dict: # uses the user fixture
    return { 
        "meal_name": "alternative",
        "entry_date": "2022-05-07",
        "meal_type": "D",
        "protein_per_100g": 1.7,
        "carbohydrates_per_100g": 20.1,
        "fat_per_100g": 0.7,
        "kcal_per_100g": 90.0,
        "food_item_mass_in_grams": 260
    }