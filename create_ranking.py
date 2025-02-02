import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('with_normalized_marks_updated.csv')

def rank_generator(df, column_name):
    """
    Rank a DataFrame by a given column and add the rank to a new column.
    
    Parameters:
    - df: The DataFrame to rank.
    - column_name: The name of the column to rank by.
    
    Returns:
    - The DataFrame with a new column 'rank_by_{column_name}' containing the rank.
    """
    # Create a new column name based on the column name
    rank_column = f'rank_by_{column_name}'
    df[rank_column] = 0  # Initialize the column

    # Filter rows where 'computer_status' is 'P'
    filtered_df = df[df['computer_status'] == 'P']

    # Rank the filtered DataFrame based on the given column
    filtered_df[rank_column] = filtered_df[column_name].rank(ascending=False, method='min')

    # Update the original DataFrame with the ranks for rows where 'computer_status' is 'P'
    df.update(filtered_df)

    return df

# Generate ranks for the specified columns
df = rank_generator(df, 'section_1_2_marks')
df = rank_generator(df, 'section_1_2_marks_with_bonous')
df = rank_generator(df, 'total_normalized_marks')

# Save the ranked DataFrame to a new CSV file
df.to_csv('ranked_output.csv', index=False)

print("Ranked data saved to 'ranked_output.csv'")
