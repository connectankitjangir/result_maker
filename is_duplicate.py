import pandas as pd

# Load the combined data
df_combined = pd.read_excel('combined_data_with_details.xlsx')

# Check for duplicates based on the 'ROLL' column
duplicates = df_combined[df_combined.duplicated(subset='ROLL', keep=False)]

# Print the duplicates if any
if not duplicates.empty:

    print("Duplicate entries found based on 'ROLL':")
    print(duplicates)
else:
    print("No duplicate entries found based on 'ROLL'.")
