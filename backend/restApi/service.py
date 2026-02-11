from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
import numpy as np
from pprint import pprint


def CalculateSummary(queryset: QuerySet):

    dataPerDay = PopulateDataPerDay(queryset)
    statisticsPerDay = DailySummary(dataPerDay)
    statisticsDailyDifference = DailyDifferenceAnalysis(statisticsPerDay)

    return statisticsPerDay, statisticsDailyDifference


"""
This function would look at the difference item types (breakfast, lunch ect) across days and calculate statistics such as mean, median etc
and return a single dictionary with the resultant values for each item type and for the whole day
it should return the stats 
"""


def DailyDifferenceAnalysis(statisticsPerDay):

    dailyDifference = {
        'consumed_date': [],
        'cumulative': {'item_mass': [], 'protein': [], 'carbohydrate': [], 'fat': [], 'kcal': [], 'item_name': []},
        'B': {'item_mass': [], 'protein': [], 'carbohydrate': [], 'fat': [], 'kcal': [], 'item_name': []},
        'L': {'item_mass': [], 'protein': [], 'carbohydrate': [], 'fat': [], 'kcal': [], 'item_name': []},
        'D': {'item_mass': [], 'protein': [], 'carbohydrate': [], 'fat': [], 'kcal': [], 'item_name': []},
        'S': {'item_mass': [], 'protein': [], 'carbohydrate': [], 'fat': [], 'kcal': [], 'item_name': []},
        'O': {'item_mass': [], 'protein': [], 'carbohydrate': [], 'fat': [], 'kcal': [], 'item_name': []},
    }

    for dailySummary in statisticsPerDay:
        dailyDifference["consumed_date"].append(dailySummary["consumed_date"])
        for item_type, nutrient_info in dailySummary.items():
            if item_type != "consumed_date":
                for macronutrient, value in nutrient_info.items():
                    dailyDifference[item_type][macronutrient].append(value)

    for item_type, nutrient_info in dailyDifference.items():
        if item_type != "consumed_date":
            for macronutrient in [
                "item_mass",
                "protein",
                "carbohydrate",
                "fat",
                "kcal",
            ]:
                if dailyDifference[item_type][macronutrient] != []:
                    dailyDifference[item_type][f"{macronutrient}Sum"] = sum(
                        dailyDifference[item_type][macronutrient]
                    )
                    dailyDifference[item_type][f"{macronutrient}Mean"] = np.mean(
                        dailyDifference[item_type][macronutrient]
                    )
                    dailyDifference[item_type][f"{macronutrient}Median"] = np.median(
                        dailyDifference[item_type][macronutrient]
                    )
                    dailyDifference[item_type][f"{macronutrient}Std"] = np.std(
                        dailyDifference[item_type][macronutrient]
                    )
                    dailyDifference[item_type][f"{macronutrient}Var"] = np.var(
                        dailyDifference[item_type][macronutrient]
                    )
                else:
                    dailyDifference[item_type][f"{macronutrient}Sum"] = 0
                    dailyDifference[item_type][f"{macronutrient}Mean"] = 0
                    dailyDifference[item_type][f"{macronutrient}Median"] = 0
                    dailyDifference[item_type][f"{macronutrient}Std"] = 0
                    dailyDifference[item_type][f"{macronutrient}Var"] = 0

                del dailyDifference[item_type][macronutrient]

    return dailyDifference


"""
This function would return a breakdown dictionary of what food items were eaten at breakfast, 
lunch etc, the sum (and not other things) of macros and energy per meal type and cumulative

"""


def DailySummary(dataPerDay):
    statisticsPerDay: list[dict] = []

    for data in dataPerDay:
        statisticOfTheDay = {
            "consumed_date": data["consumed_date"],
            "cumulative": {
                "item_mass": [],
                "protein": [],
                "carbohydrate": [],
                "fat": [],
                "kcal": [],
                "item_name": [],
            },
        }

        for meal_type, nutrient_info in data.items():
            if meal_type != "consumed_date":
                statisticOfTheDay[meal_type] = {}
                for macronutrient, valueArray in nutrient_info.items():
                    # print(nutrient_info)
                    if macronutrient != "item_name":
                        statisticOfTheDay[meal_type][f"{macronutrient}"] = sum(
                            valueArray
                        )
                        statisticOfTheDay["cumulative"][f"{macronutrient}"].append(
                            sum(valueArray)
                        )
                    else:
                        statisticOfTheDay[meal_type]["item_name"] = valueArray
                        statisticOfTheDay["cumulative"]["item_name"].append(valueArray)

        for key, value in statisticOfTheDay["cumulative"].items():
            if key != "item_name":
                statisticOfTheDay["cumulative"][key] = sum(value)

        # pprint(statisticOfTheDay, width=120, sort_dicts=False)
        statisticsPerDay.append(statisticOfTheDay)
    return statisticsPerDay


def PopulateDataPerDay(queryset: QuerySet):
    # pprint(queryset, width=60, sort_dicts=False, compact=False)

    dataPerDay: list[dict] = []

    for foodItem in queryset:
        (
            consumed_date,
            item_mass,
            protein,
            carbohydrate,
            fat,
            kcal,
            item_name,
            item_type,
        ) = foodItemParser(foodItem)

        foundDate: bool = False
        for data in dataPerDay:
            if data["consumed_date"] == consumed_date:
                foundDate = True
                # print(item_type, data.keys())
                if item_type in data.keys():
                    data[item_type]["item_mass"].append(item_mass)
                    data[item_type]["protein"].append(protein)
                    data[item_type]["carbohydrate"].append(carbohydrate)
                    data[item_type]["fat"].append(fat)
                    data[item_type]["kcal"].append(kcal)
                    data[item_type]["item_name"].append(item_name)
                else:
                    data[item_type] = {
                        "item_mass": [item_mass],
                        "protein": [protein],
                        "carbohydrate": [carbohydrate],
                        "fat": [fat],
                        "kcal": [kcal],
                        "item_name": [item_name],
                    }

        if foundDate == False:
            dataPerDay.append(
                {
                    "consumed_date": consumed_date,
                    item_type: {
                        "item_mass": [item_mass],
                        "protein": [protein],
                        "carbohydrate": [carbohydrate],
                        "fat": [fat],
                        "kcal": [kcal],
                        "item_name": [item_name],
                    },
                }
            )
    return dataPerDay


def foodItemParser(foodItem):
    consumed_dt = parse_datetime(foodItem["consumed_date"])
    consumed_date = consumed_dt.date()
    item_mass = foodItem["item_mass"]
    item_name = foodItem["description_details"]["Item_name"]
    item_type = foodItem["item_type"]

    Protein_per_100g = foodItem["description_details"]["Protein_per_100g"]
    protein = Protein_per_100g * item_mass / 100

    Carbohydrate_per_100g = foodItem["description_details"]["Carbohydrate_per_100g"]
    carbohydrate = Carbohydrate_per_100g * item_mass / 100

    Fat_per_100g = foodItem["description_details"]["Fat_per_100g"]
    fat = Fat_per_100g * item_mass / 100

    Kcal_per_100g = foodItem["description_details"]["Kcal_per_100g"]
    kcal = Kcal_per_100g * item_mass / 100

    return (
        consumed_date,
        item_mass,
        protein,
        carbohydrate,
        fat,
        kcal,
        item_name,
        item_type,
    )
