import pandas as pd

# Step 1: Load and combine data from 6 CSV files into an original DataFrame
file_paths = ["combined_parts.csv"]
original_df = pd.concat([pd.read_csv(file) for file in file_paths])

# Step 2: Load the result DataFrame from another CSV file
result_df = pd.read_excel("CGL_MAINS_2024_LINK_UNIQUE.xlsx")


# Step 3: Remove rows from the original DataFrame where the first column matches the first column in result_df
original_first_col = original_df.columns[1]
result_first_col = result_df.columns[1]

#drop duplicates
updated_original_df = original_df[~original_df[original_first_col].isin(result_df[result_first_col])]


# Step 4: Save the updated DataFrame to a new CSV file
updated_original_df.to_csv("remaining_after_main_jso.csv", index=False)

print("Updated original DataFrame saved to 'ankit_filtered_1.csv'")