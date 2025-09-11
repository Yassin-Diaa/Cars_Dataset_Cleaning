# Cars Dataset Cleaning Project


## Introduction
This project focuses on **cleaning and preprocessing a cars dataset** using **Python (Pandas, NumPy, and Regex)**.

The raw dataset contained:
- Special characters (`$`, `,`, `Nm`, `hp`, etc.)  
- Mixed text and numbers in numeric columns
- Poor text format
- Missing values  
- Duplicate rows  

The final cleaned dataset:
 [cars_dataset_cleaned.csv](./Data/cars_dataset_cleaned.csv)
---
## Technologies used
- Python
- pandas
- numpy
- re (regex)


---

##  Data Cleaning Steps
1. **Inspecting the dataset**  
   - Printed shape, missing values, summary statistics  
```python
print(df.shape)
print(df.describe())
print(df.head)
print(pd.isna(df).sum())
print(df.columns)
```
2. **Standardizing text columns**  
   - Converted `Company Names`, `Cars Names`, and `Engines` to have **title case** and removed spaces  
```python
text_cols = ["Company Names", "Cars Names","Engines"]
for col in text_cols:
    df[col] = df[col].astype(str).str.title().str.strip()
```
3. **Cleaning numeric columns**  
   - Removed special characters, spacing, and letters form these columns:  
     - `Total Speed`  
     - `Performance(0 - 100 )KM/H`  
     - `CC/Battery Capacity`
```python
num_cols = ["Total Speed", "Performance(0 - 100 )KM/H", "CC/Battery Capacity"]

for num_col in num_cols:
    df[num_col] = df[num_col].str.replace(",","").str.extract(r"(\d+)").astype(float)   
```
   - Removed `$`, `,`, `Nm`, `hp`, `~`, `.` 
   - Converted ranges (e.g., `"100-140"` → `120.0`) in these columns:
        - `Cars Prices`
        - `Torque`
        - `HorsePower`
```python
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
   
```
4. **Handling missing values**  
   - Numeric: replaced with median  
   - Categorical: replaced with `"Unknown"`  
```python
df["Cars Prices"].fillna(df["Cars Prices"].median(), inplace = True)
df["Torque"].fillna(df["Torque"].median(), inplace = True)
df["Performance(0 - 100 )KM/H"].fillna(df["Performance(0 - 100 )KM/H"].median(), inplace = True)
df["CC/Battery Capacity"].fillna("Unknown", inplace = True)   
```

5. **Removing duplicates**  
```python
df.drop_duplicates(inplace = True)   
```

6. **Exporting cleaned data**  
   - Saved as `Data/cars_dataset_cleaned.csv`
```python
df.to_csv("../Data/cars_dataset_cleaned.csv", index = False)  
```
- check out the Python cleaning script here: [data_cleaning.py](./Scripts/data.cleaning.py)
---

## What I learned


Throughout this project, I learned a lot about professional data cleaning workflows:  

- **Data inspection matters first**: I realized how important it is to start with understanding the shape of the dataset, missing values, and anomalies before jumping into cleaning.  
- **Regex & string methods**: Using regex and string functions like `.str.strip()`, `.str.replace()`, and `.str.extract()` helped me standardize messy text and numeric columns.  
- **Handling ranges**: Learned how to deal with inconsistent formats such as `"100-140"` or `"55000 / 65000"` by converting them into meaningful.  
- **Missing value strategies**: Explored when to use the median for numeric features and placeholders like `"Unknown"` for categorical features.

---

##  Conclusion  

This project gave me hands-on experience in **data cleaning using Python and pandas**.

By the end of this process, I was able to:  

- Transform a raw, inconsistent dataset into a **structured and analysis-ready CSV file**.  
- Build a **repeatable Python script**  that can be reused on similar datasets.  
- Document my workflow clearly so others can follow along and apply the same steps.  

Overall, this project taught me the importance of **clean data** as the foundation of any analysis or machine learning project. Without reliable preprocessing, insights and models would be inaccurate or misleading.  









