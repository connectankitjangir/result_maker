import pandas as pd

# Step 1: Load and combine data from 6 CSV files into an original DataFrame
file_paths = ["trash/remaining_after_main_jso.csv"]
original_df = pd.concat([pd.read_csv(file) for file in file_paths])


# Step 2: Load the result DataFrame from another CSV file
result_df = pd.read_csv("jso_part_2_output.csv")



# Step 3: Remove rows from the original DataFrame where the first column matches the first column in result_df
original_first_col = original_df.columns[1]
result_first_col = result_df.columns[1]

# Find rows in result_df where the first column matches the first column in original_df
matching_rows = result_df[result_df[result_first_col].isin(original_df[original_first_col])]

# Combine the matching rows with the original DataFrame
# updated_original_df = pd.concat([original_df, matching_rows], ignore_index=True)



# Step 4: Save the updated DataFrame to a new CSV file
matching_rows.to_csv("extra_after_harshit.csv", index=False)


print("Updated original DataFrame saved to 'ankit_filtered_1.csv'")