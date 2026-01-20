"""
Plan or summary of what I actually intend to implement

you as a user your look at the back of a food product packaging, and enter 
- proteins, fat, sugars and kcal for 100g of the product, and the weight in grams of the product that you have eaten
- then the table calculates the actual macronutrients and energy content of the food you eaten, based on the calculations 
    ->  form validation is not implemented
- also, the table may have a functionality of calculating summary of the statistics per day/week/month/year, or by the 
    time period that you request (but that will come later)




I will need to create a user model, which
    has a many to one relationship with the dietary information table, where 1 user can have more than one table (why?)

when done, think about form validation, and how to test all of this




As a part of the application, include a 
    user class, 
    permission class, 
    filtering,
    pagination
"""

# what would be cool to add is search for food items that a user has already inputted, so that you wouldn't have to insert the 
# nutrition values all over again and could just enter the mass of the food item

"""
Lets start with something simple:figure out how to create 

    1) DONE endpoint that would return all of the items of the database 
    2) DONE an endpoint that would return an item with a specific id/index

    The following functions will take a lot of space in the views file -> it may be a good 
    idea to put them in a separate file/package early on and import it into views.py

    !!!!!!!! Sum(...) returns None if there are no matching rows for that day. Subtracting None from a number raises a TypeError. !!!!!!!!!!!!

    Write an API that would be useful for the end user who could use the API/application
    Daily and weekly totals
        KINDA DONE Total kcal per day, week, and rolling 7-day average
        STRAIGHTFORWARD TO IMPLEMENT Total protein, fat, sugars per day and per week
        Day-to-day variability (consistency is often more actionable than a single number)
    Progression statistics and portion behaviour insights
        Comparison of macros/energy of average daily intake of this week vs last week (same for month and year)
        Average portion sizes by meal type & Portion drift over time (if there a meal that is eaten repeatedly)
        Foods where portion size is consistently larger than typical
        Results whether the expected food intake matches the real food intake -> need to couple the User class into the model to implement this
    Food items that stand out: Top contributors, anomaly and audit checks
        Top foods by total calories over the last 7/30/90 days
        Top foods by total sugars, or “hidden sugar” contributors
        “If you change one thing” candidates: the few items that dominate outcomes
        Flag days with unusually low or high calories
        Flag entries that look inconsistent (portion size extreme, per-100g kcal outliers)
        Missing-meal detection (helpful when users forget to log)
    Breakdown by meal type
        Calories and macros by breakfast vs lunch vs dinner vs snacks vs other
        “Snack load” as a percentage of daily calories
        Which meal contributes most sugars or most fat or proteins
    Macro balance and composition
        Macro split by calories (protein vs fat vs carbs/sugars)
        Protein density: grams of protein per 100 kcal
        “High sugar day” detection and how often it happens

"""



"""

A script to put something quick into the database (from ChatGPT because I was lazy)

import json
import datetime
from django.db import transaction
from restApi.models import DietStats

SEED_PATH = "seed_dietstats.json"

with open(SEED_PATH, "r", encoding="utf-8") as f:
    rows = json.load(f)

# Optional: wipe existing data so re-running does not duplicate rows
# DietStats.objects.all().delete()

def parse_date(value: str) -> datetime.date:
    # expects "YYYY-MM-DD"
    return datetime.date.fromisoformat(value)

objs = []
for r in rows:
    objs.append(
        DietStats(
            meal_name=str(r["meal_name"]),
            entry_date=parse_date(r["entry_date"]),
            meal_type=str(r["meal_type"]),
            protein_per_100g=float(r["protein_per_100g"]),
            carbohydrates_per_100g=float(r["carbohydrates_per_100g"]),
            fat_per_100g=float(r["fat_per_100g"]),
            kcal_per_100g=float(r["kcal_per_100g"]),
            food_item_mass_in_grams=int(r["food_item_mass_in_grams"]),
        )
    )

with transaction.atomic():
    DietStats.objects.bulk_create(objs, batch_size=1000)

print("Inserted:", len(objs))
print("Total rows in table:", DietStats.objects.count())

# Quick spot-check
for item in DietStats.objects.order_by("-entry_date")[:5]:
    print(item.id, item.entry_date, item.meal_type, item.meal_name, item.kcal_consumed)
"""