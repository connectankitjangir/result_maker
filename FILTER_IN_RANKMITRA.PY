import pandas as pd

# Read data from the CSV files
rankmitra_df = pd.read_csv('cgl_rankmitra.csv')
main_jso_df = pd.read_csv('remaining_after_main_jso.csv')

# Prepare a list to hold matching rows
matching_rows = []

# Iterate through each row in the main JSO DataFrame
for index, main_row in main_jso_df.iterrows():
    main_roll = str(main_row['ROLL'])
    main_name = str(main_row['NAME'])

    # Extract the first 2 characters of the name and the first 4 and last 2 characters of the roll
    main_name_prefix = main_name[:2]
    main_name_first_part = main_name.split(' ')[0]
    main_name_suffix = main_name[4:]  # Get the substring after the first 4 characters of the name
    
    main_roll_prefix = main_roll[:4]
    main_roll_suffix = main_roll[-2:]

    # Filter the rankmitra DataFrame for matches
    matches = rankmitra_df[
        (rankmitra_df['ROLL'].str.startswith(main_roll_prefix)) &

        (rankmitra_df['ROLL'].str.endswith(main_roll_suffix)) &
        (rankmitra_df['NAME'].str.startswith(main_name_prefix)) &
        (rankmitra_df['NAME'].str.endswith(main_name_suffix))
    ]


    # Append matching rows to the list
    for _, match_row in matches.iterrows():
        matching_rows.append(match_row)

# Create a new DataFrame from the matching rows
matching_df = pd.DataFrame(matching_rows)

# Write the matching rows to a new CSV file
matching_df.to_csv('matching_rows_in_rankmitra.csv', index=False)
