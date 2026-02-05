from django.db.models import QuerySet
from datetime import datetime, date
from django.utils.dateparse import parse_datetime
from pprint import pprint

def foodItemParser(foodItem):
    consumed_dt = parse_datetime(foodItem['consumed_date'])
    consumed_date = consumed_dt.date()
    item_mass = foodItem['item_mass']
    item_name = foodItem['description_details']['Item_name']
    item_type = foodItem['item_type']

    Protein_per_100g = foodItem['description_details']['Protein_per_100g']
    protein = Protein_per_100g * item_mass / 100

    Carbohydrate_per_100g = foodItem['description_details']['Carbohydrate_per_100g']
    carbohydrate = Carbohydrate_per_100g * item_mass / 100

    Fat_per_100g = foodItem['description_details']['Fat_per_100g']
    fat = Fat_per_100g * item_mass / 100

    Kcal_per_100g = foodItem['description_details']['Kcal_per_100g']
    kcal = Kcal_per_100g * item_mass / 100

    return (consumed_date, 
            item_mass, 
            protein, 
            carbohydrate, 
            fat, 
            kcal, 
            item_name, 
            item_type)

"""
This function takes in the the summaries list for each day and returns a single dict 
that contains the mean, median and mode of energy and macros eaten per day, and also split
into breakfast, lunch etc
"""
def CalculateAverages(summaries_list: list[dict]):
    result = summaries_list[0]

    for dailyIntake in summaries_list:
        pass

    pass

def CalculateSummary(queryset: QuerySet):

    summaries_per_day: list[dict] = []

    for foodItem in queryset:
        (consumed_date, 
            item_mass, 
            protein, 
            carbohydrate, 
            fat, 
            kcal, 
            item_name, 
            item_type) = foodItemParser(foodItem)
        # print(f'item_mass {item_mass}')
        # print(f'protein {protein}')
        # print(f'carbohydrate {carbohydrate}')
        # print(f'fat {fat}')
        # print(f'kcal {kcal}')
        # print(f'item_name {item_name}')
        # print(f'item_type {item_type}')
        
        foundDate: bool = False
        for summary in summaries_per_day:
            if summary['consumed_date'] == consumed_date:
                foundDate = True
                # print(item_type, summary.keys())
                if item_type in summary.keys():
                    summary[item_type]["item_mass"] = summary[item_type]["item_mass"] + item_mass
                    summary[item_type]["protein"] = summary[item_type]["protein"] + protein
                    summary[item_type]["carbohydrate"] = summary[item_type]["carbohydrate"] + carbohydrate
                    summary[item_type]["fat"] = summary[item_type]["fat"] + fat
                    summary[item_type]["kcal"] = summary[item_type]["kcal"] + kcal
                    summary[item_type]["item_name"].append(item_name)
                else:
                    summary[item_type] = {
                        "item_mass": item_mass, 
                        "protein": protein, 
                        "carbohydrate": carbohydrate, 
                        "fat": fat, 
                        "kcal": kcal, 
                        "item_name": [item_name], 
                    }
                summary['daily_cumulative']["item_mass"] = summary['daily_cumulative']["item_mass"] + item_mass
                summary['daily_cumulative']["protein"] = summary['daily_cumulative']["protein"] + protein
                summary['daily_cumulative']["carbohydrate"] = summary['daily_cumulative']["carbohydrate"] + carbohydrate
                summary['daily_cumulative']["fat"] = summary['daily_cumulative']["fat"] + fat
                summary['daily_cumulative']["kcal"] = summary['daily_cumulative']["kcal"] + kcal
                summary['daily_cumulative']["item_name"].append(item_name)

        if foundDate == False:
            summaries_per_day.append(
                {
                    'consumed_date' : consumed_date,
                    item_type: {
                        "item_mass": item_mass, 
                        "protein": protein, 
                        "carbohydrate": carbohydrate, 
                        "fat": fat, 
                        "kcal": kcal, 
                        "item_name": [item_name], 
                    },
                    'daily_cumulative': {
                        "item_mass": item_mass, 
                        "protein": protein, 
                        "carbohydrate": carbohydrate, 
                        "fat": fat, 
                        "kcal": kcal, 
                        "item_name": [item_name], 
                    }
                }
            )
    print(type(summaries_per_day))
    # pprint(summaries_per_day, width=120, sort_dicts=False)


    