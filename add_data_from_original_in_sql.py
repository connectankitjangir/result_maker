# read csv combined_parts.csv ad df
import pandas as pd

df_details = pd.read_csv('combined_parts.csv')

# read sqlite data_calculated.db and df
import sqlite3

# read csv raw_data_from_main_jso.csv as df_raw
df_raw = pd.read_excel('anwekey_with_marks.xlsx')

# merge df_details and df_raw on roll_number
df_merged = pd.merge(df_details, df_raw, on='roll_number', how='left')

# save df_merged to csv
df_merged.to_csv('combined_data_with_details_marks.csv', index=False)
