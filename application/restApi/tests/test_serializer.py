import pytest
import logging
import datetime
from hypothesis import given, strategies as st
import unicodedata
from rest_framework.test import APIClient

logger = logging.getLogger(__name__)


# this function is absolutely disgusting, but it works, and at this stage rewriting is just not worth it
def variable_payload(
        meal_name='test',
        entry_date=datetime.date.today(), # when creating further tests, be aware that this parameter may not be there in there
        meal_type='O',
        protein_per_100g=30.0,
        fat_per_100g=30.0,
        sugar_per_100g=30.0,
        kcal_per_100g=30.0,
        food_item_mass_in_grams=30,
        **kwargs
        ):
    
    reply = {
        "meal_name": meal_name,
        "entry_date": entry_date,
        "meal_type": meal_type,
        "protein_per_100g": protein_per_100g,
        "sugar_per_100g": sugar_per_100g,
        "fat_per_100g": fat_per_100g,
        "kcal_per_100g": kcal_per_100g,
        "food_item_mass_in_grams": food_item_mass_in_grams
    }

    if "alt_protein" in kwargs: reply['protein_per_100g'] = kwargs['alt_protein']
    if "alt_sugar" in kwargs:reply['sugar_per_100g'] = kwargs['alt_sugar']
    if "alt_fat" in kwargs: reply['fat_per_100g'] = kwargs['alt_fat']
    if "alt_kcal" in kwargs: reply['kcal_per_100g'] = kwargs['alt_kcal']
    if "alt_item_mass" in kwargs: reply['food_item_mass_in_grams'] = kwargs['alt_item_mass']

    return reply


@pytest.mark.django_db
def test_date_edge_cases(api_client) -> None:
    date_too_far = datetime.date.today() + datetime.timedelta(days=7)
    payload = variable_payload(entry_date=date_too_far)
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 400
    assert response_create.data['non_field_errors'][0] == ('You '
    'can not enter items more than a week in a future')

    date_just_in_time = datetime.date.today() + datetime.timedelta(days=6, 
                                                                   hours=23, 
                                                                   minutes=59, 
                                                                   milliseconds=100)
    payload = variable_payload(entry_date=date_just_in_time)
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201

@pytest.mark.django_db
def test_meal_name_edge_cases(api_client) -> None:

    """
    asserts below check that the DietStatsSerializer validator correctly trims 
    the whitespaces of the food item entry
    """
    
    payload = variable_payload(meal_name='A Typical valid name')
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    assert response_create.data['meal_name'] == 'A Typical valid name'


    payload = variable_payload(meal_name='   has left whitespace')
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    assert response_create.data['meal_name'] == 'has left whitespace'

    payload = variable_payload(meal_name='has right whitespace    ')
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    assert response_create.data['meal_name'] == 'has right whitespace'

    payload = variable_payload(meal_name='   has left and right whitespace    ')
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    assert response_create.data['meal_name'] == 'has left and right whitespace'

    payload = variable_payload(meal_name='   has   whitespace   inside    ')
    response_create = api_client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 201
    assert response_create.data['meal_name'] == 'has whitespace inside'

    """
    these one check that any character outside of the allowlist_string 
    ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ")
    are not accepted
    """
    illegal_name = '!@#$%^&*()'
    payload = variable_payload(meal_name=illegal_name)
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

check_string = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "1234567890 "
    "\t"        # U+0009 tab
    "\x0b"      # U+000B vertical tab
    "\x0c"      # U+000C form feed
    "\r"        # U+000D carriage return
    "\x1c\x1d\x1e\x1f"  # U+001C..U+001F separators
    "\x85"      # U+0085 next line (NEL)
    "\xa0"      # U+00A0 no-break space (NBSP)
    "\n"        # U+000A end of line
)
"""
I am including these unicode characters here because of the following logic
    1) Python's strip and split treats these characters as whitespace and removes them (which is fine)
    2) When the validator parses through the string and sees any of these separators, it returns the validation error
    -> the problem of this specific test is that when a string is "<some valid character><one of those separator>", 
        after " ".join(n.strip().split()) the string becomes  "<some valid character>", and the APIClient returns code 201
        thus failing the response_create.status_code == 400, which is annoying
"""

@pytest.mark.django_db
@given(
    illegal_name=st.text(
        min_size=1, max_size=99
        ).filter(
            lambda n: not (set(n) <= set(check_string))
            ).filter(
                lambda n: " ".join(n.strip().split()) != '')
    )
def test_meal_name_hypothesis_testing(illegal_name) -> None:

    payload = variable_payload(meal_name=illegal_name)
    client = APIClient()
    response_create = client.post('/diet/', data=payload, format="json")
    if response_create.status_code != 400:
        codepoints = " ".join(f"U+{ord(ch):04X}" for ch in illegal_name)
        logger.info("codepoints: %s", codepoints)

        details = [f"ascii symbol: {ascii(ch)}; Unicode name: {unicodedata.name(ch, '<no name>')}; Unicode codepoint: U+{ord(ch):04X}" for ch in illegal_name]
        logger.info("chars:\n%s", "\n".join(details))

        logger.info(f"response_create.status_code: {response_create.status_code}" )
    assert response_create.status_code == 400
    try:
        assert response_create.data['non_field_errors'][0] == ("Food item contains illegal characters. "
                                                 "Use only letters and numbers")
    except:
        assert response_create.data['meal_name'][0] == 'Null characters are not allowed.'


"""
What else needs to be checked?

        Check if other data types can also be permitted (decimals, floats, integers)

        the food type is the last thing to check


"""

@pytest.mark.django_db
@given(macro_too_high=(st.integers(min_value=101) | st.floats(min_value=100.00000000000001)).filter(lambda n: float('-inf') < n < float('inf')))
def test_macro_too_high_hypothesis_testing(macro_too_high) -> None:
    # logger.info(f"macro_too_high: {macro_too_high}" )
    client = APIClient()

    macro_too_high = {
        "alt_protein": macro_too_high,
        "alt_sugar": macro_too_high,
        "alt_fat": macro_too_high,
    }

    for key, value in macro_too_high.items():
        payload = variable_payload(**{key: value})
        response_create = client.post('/diet/', data=payload, format="json")
        assert response_create.status_code == 400 
        assert response_create.data['non_field_errors'][0] == "100 grams of food can not have more than a 100g of a macronutrient"

@pytest.mark.django_db
@given(macro_too_low=(st.integers(max_value=-1) | st.floats(max_value=-0.00000000000001)).filter(lambda n: float('-inf') < n < float('inf')))
def test_macro_too_low_hypothesis_testing(macro_too_low) -> None:
    client = APIClient()

    macro_too_low = {
        "alt_protein": macro_too_low,
        "alt_sugar": macro_too_low,
        "alt_fat": macro_too_low,
        "alt_kcal": macro_too_low,
        "alt_item_mass": macro_too_low,
    }

    for key, value in macro_too_low.items():
        payload = variable_payload(**{key: value})
        response_create = client.post('/diet/', data=payload, format="json")
        assert response_create.status_code == 400 
        assert response_create.data['non_field_errors'][0] == 'nutrition values can not be negative'
        

@pytest.mark.django_db
@given(
    macro_too_high=(
        st.integers(min_value=5001) | st.floats(min_value=5000.00001)
        ).filter(
            lambda n: float('-inf') < n < float('inf')
            )
    )
def test_item_mass_too_high_hypothesis_testing(macro_too_high) -> None:
    # logger.info(f"macro_too_high: {macro_too_high}" )
    client = APIClient()

    payload = variable_payload(food_item_mass_in_grams=macro_too_high)
    response_create = client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 400 
    assert response_create.data['non_field_errors'][0] == "The food mass or kcal value is too big."

@pytest.mark.django_db
@given(macro_too_high=(st.integers(min_value=5001) | st.floats(min_value=5000.00001)).filter(lambda n: float('-inf') < n < float('inf')))
def test_kcal_too_high_hypothesis_testing(macro_too_high) -> None:
    # logger.info(f"macro_too_high: {macro_too_high}" )
    client = APIClient()

    payload = variable_payload(kcal_per_100g=macro_too_high)
    response_create = client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 400 
    assert response_create.data['non_field_errors'][0] == "The food mass or kcal value is too big."



@pytest.mark.django_db
@given(
    macro_list=st.lists(
        st.integers(
            min_value=0, 
            max_value=100
            ) | 
        st.floats(
            min_value=0, 
            max_value=100
            ).filter(lambda n: float('-inf') < n < float('inf')), 
        min_size=3,
        max_size=3,
        ).filter(lambda n: sum(n) > 100)
)
def test_macros_sum_too_high_hypothesis_testing(macro_list) -> None:
    # logger.info(f" {macro_list}; their sum is {sum(macro_list)}" )

    protein, sugar, fat = macro_list

    macro_sum_too_high = {
        "alt_protein": protein,
        "alt_sugar": sugar,
        "alt_fat": fat,
    }

    client = APIClient()
    payload = variable_payload(**macro_sum_too_high)
    response_create = client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 400 
    assert response_create.data['non_field_errors'][0] == "Sum of macronutrients per 100g can not 100g"


allowed_meal_types = "BLDSO"
@pytest.mark.django_db
@given(
    illegal_type=st.text().filter(
            lambda n: not (set(n) <= set(allowed_meal_types))
            )
    )
def test_meal_type_hypothesis_testing(illegal_type) -> None:
    client = APIClient()

    payload = variable_payload(meal_type=illegal_type)
    response_create = client.post('/diet/', data=payload, format="json")
    assert response_create.status_code == 400 
    assert response_create.data['meal_type'][0] == f'"{illegal_type}" is not a valid choice.'
