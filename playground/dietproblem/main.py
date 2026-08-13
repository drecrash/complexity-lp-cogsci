# just messing around to learn pulp
import pulp as pl
from pulp import *
import json
import pandas as pd


FOOD_DATA_CSV = "food-data-fin.csv"
food_df = pd.read_csv(FOOD_DATA_CSV)

food_df.dropna(how="all", inplace=True)
food_df = food_df[food_df["Caloric Value"] > 20]

with open("nutrient_req.json", "r") as f:
    nutreq = json.load(f)

with open("nutrient_max.json", "r") as f:
    nutmax = json.load(f)

all_foods = list(food_df["food"])
food_costs = food_df.set_index('food')['cost'].to_dict()
food_nutrients = food_df.set_index("food").to_dict(orient="index")

for nut, req in nutreq.items():
    if nut not in food_df.columns.to_list():
        print(nut)

prob = LpProblem("diet", LpMaximize)

food_amts = pulp.LpVariable.dicts("b", all_foods)

for food in all_foods:
    food_amts[food].bounds(0, None)
#prob += lpSum([food_amts[food] * food_costs[food] for food in all_foods])
prob += lpSum([food_amts[food] * (food_df.loc[food_df["food"] == food]).iloc[0]["Protein"] for food in all_foods])


for nutrient, requirement in nutreq.items():
    collective_nutrients = []
    for food in all_foods:
        try:
            collective_nutrients.append([food_amts[food]*(food_df.loc[food_df["food"] == food]).iloc[0][nutrient]])
        except:
            print(food)
            raise

    prob += lpSum(collective_nutrients) >= requirement

caloric_limit = 2000
prob += lpSum([food_amts[food]*(food_df.loc[food_df["food"] == food]).iloc[0]["Caloric Value"] for food in all_foods]) <= caloric_limit

status = prob.solve()

print(LpStatus[status])

def get_unit(nutrient):
    unit = "g"
    if (nutrient == "Caloric Value"):
        unit = "kcal"

    return unit

total_nutrients = {}
for name, var in food_amts.items():
    val = var.value()

    if val == None:
        print(name)

    if (val != None) and val > 0:


        print(f"{name}: {round(var.value()*100,5)}g")

        item_nutrients = dict(sorted(food_nutrients[name].items(), key=lambda item: item[1],reverse=True))
        for nutrient, amt in item_nutrients.items():
            if nutrient in total_nutrients:
                total_nutrients[nutrient] += (amt*val)
            else:
                total_nutrients[nutrient] = (amt*val)
        print("\n\n")

for nutrient, amt in total_nutrients.items():

    if (nutrient not in ["Unnamed", "Unamed: 0.1", "Nutritional Density"]):
        print(f"{nutrient}: {round(amt,3)}{get_unit(nutrient)}")