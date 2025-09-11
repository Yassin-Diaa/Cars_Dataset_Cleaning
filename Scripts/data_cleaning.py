import pandas as pd
import numpy as np
import re

df = pd.read_csv("../Data/Cars Datasets 2025.csv", encoding = "latin1")

# Inspecting the data

print(df.shape)
print(df.describe())
print(df.head)
print(pd.isna(df).sum())
print(df.columns)

# Standardizing text columns

text_cols = ["Company Names", "Cars Names","Engines"]
for col in text_cols:
    df[col] = df[col].astype(str).str.title().str.strip()

# Cleaning numeric columns

num_cols = ["Total Speed", "Performance(0 - 100 )KM/H", "CC/Battery Capacity"]

for num_col in num_cols:
    df[num_col] = df[num_col].str.replace(",","").str.extract(r"(\d+)").astype(float)

df["Cars Prices"] = (
    df["Cars Prices"]
    .str.replace("$","", regex = False)
    .str.replace(",","")
    .str.strip()
)

df["HorsePower"] = (
    df["HorsePower"]
    .str.replace("hp","", regex = False)
    .str.replace("HP","", regex = False)
    .str.replace(",","")
    .str.replace("~","", regex = False)
    .str.replace(".","", regex = False)
    .str.strip()
)

df["Torque"] = (
    df["Torque"]
    .str.replace("Nm", "", regex = False)
    .str.replace(",", "", regex = False)
    .str.replace("+", "", regex = False)
    .str.replace(r"[A-Za-z]", "", regex = True)
    .str.replace(r"[()]", "", regex = True)
    .str.strip()
)

def clean_column (column_value):

    if isinstance(column_value, str):

        column_value = (
            column_value.replace("", "-")
            .replace("/", "-")
            .replace("–", "-")
            .replace("—", "-")
            .replace("", "-")
            .replace("", "-")
        )

        column_value = re.sub(r"[()]", "", column_value)
        column_value = re.sub(r"~", "", column_value)
        column_value = re.sub(r"[A-Za-z]", "", column_value)
        column_value = column_value.strip()

        parts =column_value.split("-")
        parts = [float(p) for p in parts if p.strip() != ""]

        if len(parts) == 2:
            return np.mean(parts)
        elif len(parts) == 1:
            return parts[0]
        else:
            return np.nan

df["Torque"] = df["Torque"].apply(clean_column)
df["Cars Prices"] = df["Cars Prices"].apply(clean_column)
df["HorsePower"] = df["HorsePower"].apply(clean_column)

# Handling missing values

df["Cars Prices"].fillna(df["Cars Prices"].median(), inplace = True)
df["Torque"].fillna(df["Torque"].median(), inplace = True)
df["Performance(0 - 100 )KM/H"].fillna(df["Performance(0 - 100 )KM/H"].median(), inplace = True)
df["CC/Battery Capacity"].fillna("Unknown", inplace = True)

# Removing duplicates

df.drop_duplicates(inplace = True)

# Saving cleaned data

df.to_csv("../Data/cars_dataset_cleaned.csv", index = False)

















