import pandas as pd
import re
from datetime import datetime


# Import the CSV file into a DataFrame
df = pd.read_csv("C:/Users/Klara/Documents/prace_temporary/DEFID2/exact_polygons.csv", low_memory=False)

# Print the table
print(df)

#1.) SURVEY DATE START
# Add a new column
df["survey_start_date"] = pd.to_datetime(df["survey_date"])
df["survey_end_date"] = pd.to_datetime(df["survey_date"])
# Replace 'your_column' with the name of the column you want to modify
df['survey_date_precision'] = df['survey_date_precision'].str.replace('+/-', '', regex=False)
df['survey_date_precision'] = df['survey_date_precision'].str.replace(' days', '', regex=False)


# Define a function to update the START_date based on the other_column value
def update_start_date(row):
    if row["survey_date_precision"] == "exact":
        return row["survey_start_date"]  # No change if other_column is "exact"
    else:
        try:
            days_to_subtract = int(row["survey_date_precision"])
            return pd.to_datetime(row["survey_start_date"]) - pd.DateOffset(days=days_to_subtract)
        except ValueError:
            return row["survey_start_date"]  # No change for invalid or non-numeric values

# Apply the update_target_date function to the DataFrame
df["survey_start_date"] = df.apply(update_start_date, axis=1)

#2.) SURVEY DATE END
# Define a function to update the END_date based on the other_column value
def update_start_date(row):
    if row["survey_date_precision"] == "exact":
        return row["survey_end_date"]  # No change if other_column is "exact"
    else:
        try:
            days_to_add = int(row["survey_date_precision"])
            return pd.to_datetime(row["survey_end_date"]) + pd.DateOffset(days=days_to_add)
        except ValueError:
            return row["survey_end_date"]  # No change for invalid or non-numeric values

# Apply the update_target_date function to the DataFrame
df["survey_end_date"] = df.apply(update_start_date, axis=1)


#3.) ADDING NEW EMPTY COLUMNS
df['data_provider'] = ""
df['affiliation'] = ""
df['source'] = ""

# #adDing columns for trigger dates - END and START
# df["trigger_prim_date_start"] = pd.to_datetime(df[""])
# df["trigger_prim_date_end"] = pd.to_datetime(df[""])
#
# df["trigger_seco_date_start"] = pd.to_datetime(df[""])
# df["trigger_seco_date_end"] = pd.to_datetime(df[""])


import pandas as pd
import numpy as np
import pandas as pd

#4.) TRIGGER PRIMARY DATE START
def fill_dates_start(row):
    date_column = row["trigger_primary_date"]
    if pd.isna(date_column) or date_column == -1:
        return np.nan  # Return NaN if the date is missing
    if "/" in row["trigger_primary_date"]:
        parts = row["trigger_primary_date"].split("/")
        if len(parts) == 3:
            # Case 1: Date is in the format yyyy/mm/dd
            return pd.to_datetime(row["trigger_primary_date"]).strftime("%d.%m.%Y")
        elif len(parts) == 2:
            if len(parts[0]) == 4:
                # Case 4: Date is in the format yyyy/mm
                return pd.to_datetime(row["trigger_primary_date"]).strftime("%d.%m.%Y")
            else:
                # Case 3: Date is in the format mm/yyyy
                return pd.to_datetime(row["trigger_primary_date"]).replace(day=1).strftime("%d.%m.%Y")
    elif "-" in row["trigger_primary_date"]:
        parts = row["trigger_primary_date"].split("-")
        if len(parts) == 2:
            try:
                start_year = int(parts[0])
                # Case 2: Date is in the format yyyy-yyyy
                return pd.to_datetime(f"{start_year}-01-01").strftime("%d.%m.%Y")
            except ValueError:
                pass
    elif len(row["trigger_primary_date"]) == 4:
        # Case 5: Date is a 4-digit year
        return pd.to_datetime(f"{row['trigger_primary_date']}-01-01").strftime("%d.%m.%Y")

    # Default case: Return the original value if none of the conditions match
    return row["trigger_primary_date"]

df["trigger_prim_date_start"] = df.apply(fill_dates_start, axis=1)


#5.) TRIGGER PRIMARY DATE END

def fill_dates_end(row):
    date_column = row["trigger_primary_date"]
    if pd.isna(date_column) or date_column == -1:
        return np.nan  # Return NaN if the date is missing
    if "/" in row["trigger_primary_date"]:
        parts = row["trigger_primary_date"].split("/")
        if len(parts) == 3:  # Case 1: Date in the format YYYY/MM/DD
            return f"{parts[2]}.{parts[1]}.{parts[0]}"
        elif len(parts) == 2:  # Case 4 and 5: Date in the format YYYY/MM or YY/MM
            year = int(parts[0])
            month = int(parts[1])
            if year < 100:
                year += 2000  # Convert YY to YYYY
            if month < 1 or month > 12:
                raise ValueError("Invalid month")
            last_day = pd.Timestamp(year, month, 1) + pd.DateOffset(months=1, days=-1)
            return last_day.strftime("%d.%m.%Y")
    elif "-" in row["trigger_primary_date"]:
        years = row["trigger_primary_date"].split("-")
        if len(years) == 2:  # Case 2: Date range
            end_year = int(years[1])
            return f"31.12.{end_year}"
    elif "/" not in row["trigger_primary_date"]:
        try:
            year = int(row["trigger_primary_date"])
            return f"31.12.{year}"  # Case 3 and 5: Just a year
        except ValueError:
            pass
    return row["trigger_primary_date"]  # No change for other cases

df["trigger_prim_date_end"] = df.apply(fill_dates_end, axis=1)





print(df)

# Save the modified DataFrame to a new CSV file (optional)
df.to_csv("C:/Users/Klara/Documents/prace_temporary/DEFID2/modified_data.csv", index=False)
