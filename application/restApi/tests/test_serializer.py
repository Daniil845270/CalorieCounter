import pytest
import logging
import datetime
from hypothesis import given, strategies as st

logger = logging.getLogger(__name__)

# one thing to test is whether the fields accept the values of appropriate type 
# (int but not char) and of appropriate format (especially for date)

def variable_date_payload(
        meal_name='test',
        entry_date=datetime.date.today(), # when creating further tests, be aware that this parameter may not be there in there
        meal_type='O',
        protein_per_100g=30.0,
        fat_per_100g=30.0,
        kcal_per_100g=30.0,
        food_item_mass_in_grams=30,
        ):
    return {
        "meal_name": meal_name,
        "entry_date": entry_date,
        "meal_type": meal_type,
        "protein_per_100g": protein_per_100g,
        "carbohydrates_per_100g": 30.0,
        "fat_per_100g": fat_per_100g,
        "kcal_per_100g": kcal_per_100g,
        "food_item_mass_in_grams": food_item_mass_in_grams
    }

@pytest.mark.django_db
def test_date_edge_cases(api_client) -> None:
    date_too_far = datetime.date.today() + datetime.timedelta(days=7)
    payload = variable_date_payload(entry_date=date_too_far)
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 400
    assert response_create.data['non_field_errors'][0] == ('You '
    'can not enter items more than a week in a future')

    date_just_in_time = datetime.date.today() + datetime.timedelta(days=6, 
                                                                   hours=23, 
                                                                   minutes=59, 
                                                                   milliseconds=100)
    payload = variable_date_payload(entry_date=date_just_in_time)
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    # logger.info(f"{response_create}")


    # logger.info(f"!!!!!!!!!!!!!!!!!!!!")
    # logger.info(f"{response_create}")
    # logger.info(f"{response_create.data}")
    # logger.info(f"!!!!!!!!!!!!!!!!!!!!")

@pytest.mark.django_db
def test_meal_name_edge_cases(api_client) -> None:

    """
    asserts below check that the DietStatsSerializer validator correctly trims 
    the whitespaces of the food item entry
    """
    
    payload = variable_date_payload(meal_name='A Typical valid name')
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    assert response_create.data['meal_name'] == 'A Typical valid name'


    payload = variable_date_payload(meal_name='   has left whitespace')
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    assert response_create.data['meal_name'] == 'has left whitespace'

    payload = variable_date_payload(meal_name='has right whitespace    ')
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    assert response_create.data['meal_name'] == 'has right whitespace'

    payload = variable_date_payload(meal_name='   has left and right whitespace    ')
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    assert response_create.data['meal_name'] == 'has left and right whitespace'

    payload = variable_date_payload(meal_name='   has   whitespace   inside    ')
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    assert response_create.data['meal_name'] == 'has whitespace inside'

    """
    these one check that any character outside of the allowlist_string 
    ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ")
    are not accepted
    """
    illegal_name = '!@#$%^&*()'
    payload = variable_date_payload(meal_name=illegal_name)
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 400
    assert response_create.data['non_field_errors'][0] == ("Food item contains illegal characters. "
                                                "Use only letters and numbers")



"""
hypothesis testing: generate me a string that
    1) it must 1 and 100 characters
    2) if it includes a character from the allowlist_string, it must include a character that is not in it
    3) if it includes only the characters from the allowlist_string, this string must be rejected
    4) if it consists of only whitespaces, it must be rejected
    5) everything else is permitted

"borrowed" the solution for 2 and 3 from here https://stackoverflow.com/questions/28997056/return-true-if-all-characters-in-a-string-are-in-another-string
"""

check_string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 "
@pytest.mark.django_db
@given(illegal_name=st.text(min_size=1, max_size=99)).filter(lambda n: " ".join(n.strip().split()) != '').filter(lambda n: not (set(n) <= set(check_string)))
def test_meal_name_hypothesis_testing(api_client, illegal_name) -> None:
    """
    these one check that any character outside of the allowlist_string 
    ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ")
    are not accepted
    """
    payload = variable_date_payload(meal_name=illegal_name)
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 400
    logger.info(f"{response_create}")
    logger.info(f"{response_create.data}")
    assert response_create.data['non_field_errors'][0] == ("Food item contains illegal characters. "
                                                "Use only letters and numbers")
    





