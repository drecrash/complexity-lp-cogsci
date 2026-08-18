import pulp
from pulp import *
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.patches as mpatches


# subjects are AI generated, thanks claude
subjects = {
  "Mathematics": {
    "priority": 10,
    "prerequisites": [],
    "min": 0.5,
    "max": 2.5
  },
  "Reading & Writing": {
    "priority": 10,
    "prerequisites": [],
    "min": 0.5,
    "max": 2.0
  },
  "Science": {
    "priority": 9,
    "prerequisites": ["Mathematics"],
    "min": 0.5,
    "max": 2.0
  },
  "History": {
    "priority": 8,
    "prerequisites": ["Reading & Writing"],
    "min": 0.25,
    "max": 1.5
  },
  "English / Literature": {
    "priority": 8,
    "prerequisites": ["Reading & Writing"],
    "min": 0.25,
    "max": 1.5
  },
  "Critical Thinking / Logic": {
    "priority": 8,
    "prerequisites": ["Mathematics", "Reading & Writing"],
    "min": 0.25,
    "max": 1.5
  },
  "Civics / Government": {
    "priority": 7,
    "prerequisites": ["History", "Reading & Writing"],
    "min": 0,
    "max": 1.0
  },
  "Geography": {
    "priority": 7,
    "prerequisites": ["History"],
    "min": 0,
    "max": 1.0
  },
  "Biology": {
    "priority": 7,
    "prerequisites": ["Science"],
    "min": 0.25,
    "max": 1.5
  },
  "Chemistry": {
    "priority": 7,
    "prerequisites": ["Science", "Mathematics"],
    "min": 0.25,
    "max": 2.0
  },
  "Physics": {
    "priority": 7,
    "prerequisites": ["Science", "Mathematics"],
    "min": 0.25,
    "max": 2.0
  },
  "Foreign Language": {
    "priority": 7,
    "prerequisites": ["Reading & Writing"],
    "min": 0.5,
    "max": 1.5
  },
  "Statistics": {
    "priority": 6,
    "prerequisites": ["Mathematics"],
    "min": 0.25,
    "max": 2.0
  },
  "Economics": {
    "priority": 6,
    "prerequisites": ["Mathematics", "History"],
    "min": 0,
    "max": 1.5
  },
  "Computer Science": {
    "priority": 6,
    "prerequisites": ["Mathematics", "Critical Thinking / Logic"],
    "min": 0.5,
    "max": 3.0
  },
  "Health & Physical Education": {
    "priority": 6,
    "prerequisites": ["Biology"],
    "min": 0,
    "max": 1.0
  },
  "Psychology": {
    "priority": 5,
    "prerequisites": ["Biology", "Reading & Writing"],
    "min": 0,
    "max": 1.0
  },
  "Philosophy": {
    "priority": 5,
    "prerequisites": ["Critical Thinking / Logic", "Reading & Writing"],
    "min": 0,
    "max": 1.0
  },
  "Art": {
    "priority": 5,
    "prerequisites": ["Reading & Writing"],
    "min": 0,
    "max": 2.0
  },
  "Music": {
    "priority": 5,
    "prerequisites": ["Mathematics"],
    "min": 0,
    "max": 2.0
  },
  "Calculus": {
    "priority": 4,
    "prerequisites": ["Mathematics", "Statistics"],
    "min": 0.5,
    "max": 2.5
  },
  "Drama / Theater": {
    "priority": 4,
    "prerequisites": ["Reading & Writing"],
    "min": 0,
    "max": 1.0
  },
  "Home Economics": {
    "priority": 4,
    "prerequisites": ["Mathematics", "Biology"],
    "min": 0,
    "max": 0.5
  },
  "Astronomy": {
    "priority": 3,
    "prerequisites": ["Physics", "Mathematics"],
    "min": 0,
    "max": 1.0
  },
  "Woodshop / Shop Class": {
    "priority": 3,
    "prerequisites": ["Mathematics", "Physics"],
    "min": 0,
    "max": 0.75
  }
}

# e_t
energy = {
    "morning": 2,
    "afternoon": 3,
    "evening": 1
}

T_max = 9

subject_names = list(subjects.keys())

prob = LpProblem("performance", LpMaximize)

time_vars = []


def plot_schedule(schedule):

    colors = ["r","g","b"]

    
    for subject in subject_names:
        x = subject
        sum_ = 0
        for i, time in enumerate(energy):
            y = schedule[subject][time]
            plt.bar(x,y,bottom=sum_,color=colors[i])
            sum_ += y

    morn = mpatches.Patch(color='red', label='Morning')
    aft = mpatches.Patch(color='green', label='Afternoon')
    even = mpatches.Patch(color='blue', label='Evening')
    plt.legend(handles=[morn, aft, even], loc="upper right")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.xlabel("Subjects")
    plt.ylabel("Hours")

    plt.show()

for t_ in energy:
    lp_var = pulp.LpVariable.dicts(f"x_{t_}", subject_names, lowBound=0)
    time_vars.append({
        "time": t_,
        "dict": lp_var
    })


# Set up objective function


prob += lpSum([
        subjects[s]["priority"]*energy[time_dict["time"]]*time_dict["dict"][s]
        for time_dict in time_vars
        for s in subject_names
        ])



# Minimum and Maximum Time Constraints
for s in subject_names:

    prob += lpSum([
        time_dict["dict"][s]
        for time_dict in time_vars
    ]) >= subjects[s]["min"], f"{s}_min"

    prob += lpSum([
        time_dict["dict"][s]
        for time_dict in time_vars
    ]) <= subjects[s]["max"], f"{s}_max"

# Max Total Time Constraint


prob += lpSum([
        time_dict["dict"][s]
        for time_dict in time_vars
        for s in subject_names
        ]) <= T_max, f"max_time"

# Prerequisite Constraint

decision_y = pulp.LpVariable.dicts("y", subject_names, cat="Binary")


for s in subject_names:
    prob += lpSum([
        time_dict["dict"][s] for time_dict in time_vars
    ]) <= (T_max*decision_y[s])


    for j in subjects[s]["prerequisites"]:
        prob += decision_y[s] <= decision_y[j], f"prereq_cond_{j}_for_{s}"


# Time Chunk Constraint 
for time_dict in time_vars:
    chunk_max = T_max / len(energy)
    prob += lpSum([
        time_dict["dict"][s]
        for s in subject_names
    ]) <= chunk_max, f"slot_budget_{time_dict["time"]}"


status = prob.solve()

print(LpStatus[status])

print("Schedule")
print("----------")
subj_totals = {}
for time_dict in time_vars:
    print("\n\n")
    print(time_dict["time"],":")
    for subject, var in time_dict["dict"].items():

        if subject not in subj_totals:
            subj_totals[subject] = {}
            subj_totals[subject]["tot"] = 0

        val = var.value()
        print(f"{subject}: {val}h")
        subj_totals[subject][time_dict["time"]] = val
        subj_totals[subject]["tot"] += val

print("\n\n")
print("Totals")
print("----------")

for subject, value_ in subj_totals.items():
    print(f"{subject}: {value_["tot"]}h")

print("\n\n")
print("Shadow Prices")
print("\n")
for name, constraint in prob.constraints.items():
    shadow = constraint.pi
    if shadow != 0:
        print(f"{name}: {constraint.pi}")


plot_schedule(subj_totals)
