import pandas as pd
import re
from datetime import datetime


# Import the CSV file into a DataFrame
df = pd.read_csv("C:/Users/Klara/Documents/prace_temporary/DEFID2/modified_data.csv", low_memory=False)
print(df)
# Assuming you have a DataFrame called 'df' and want unique values from the 'column_name' column
unique_values = df['trigger_prim_date_end'].drop_duplicates()
print(unique_values)
unique_values = df['trigger_primary_date'].drop_duplicates()
print(unique_values)
