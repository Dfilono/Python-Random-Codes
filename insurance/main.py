import pandas as pd
import numpy as np

# read dataset
df = pd.read_csv('insurance.csv', skiprows = 1, delimiter=',', names = ["Age", "Sex", "BMI", "Children", "Smoker", "Region", "Charges"])

# calculate the average age of the dataset
total_age = 0
for i in df["Age"]:
    total_age += i

avg_age = total_age/len(df["Age"]) 

print(f"The average age of the patients in the dataset are: {avg_age}")

# find the occurence of each region in the dataset
regions = {}
for i in df["Region"]:
    if i not in regions:
        regions[i] = 1
    else:
        regions[i] += 1

for i in regions:
    print(f"The {i} region is represented {regions[i]} times in the dataset.")

# compare insurance costs for smokers vs non-smokers in the dataset
smoker = 0
smoker_chg = 0
non_smoker = 0
non_smoker_chg = 0

for i in range(len(df["Smoker"])):
    if df["Smoker"][i] == "yes":
        smoker_chg += df["Charges"][i]
        smoker += 1
    else:
        non_smoker_chg += df["Charges"][i]
        non_smoker += 1

avg_smoker = round(smoker_chg/smoker, 2)
avg_non_smoker = round(non_smoker_chg/non_smoker, 2)

print(f"The out of {smoker} smokers and {non_smoker} non-smokers, the avgs insurance cose for smokers was ${avg_smoker} and ${avg_non_smoker} for non-smokers.")


# find the avg age of someone who has at least one child
parent = 0
age = 0

for i in range(len(df["Children"])):
    if df["Children"][i] >= 1:
        parent += 1
        age += df["Age"][i]

avg_parent = round(age/parent)

print(f"Out of {parent} parents, the average age of them is {avg_parent} years old.")