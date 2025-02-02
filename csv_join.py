import pandas as pd

# Initialize an empty DataFrame to hold the combined data
combined_data = pd.DataFrame()

# Loop through the CSV files from part_1.csv to part_20.csv
for i in range(1, 21):
    file_path = f"part_{i}.csv"
    # Read each CSV file and append it to the combined_data DataFrame
    df = pd.read_csv(file_path)
    combined_data = pd.concat([combined_data, df], ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_data.to_csv("combined_parts.csv", index=False)
