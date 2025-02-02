import pandas as pd

def normalize_marks(df, marks_column, section_name):
    """
    Normalizes the marks for a specific section in the dataframe.
    
    Parameters:
    - df: The dataframe with exam data.
    - marks_column: The column to normalize (e.g., 'section_1_marks_with_bonous').
    - section_name: The name of the section to handle in the output (e.g., 's1', 's2', 'comp').
    
    Returns:
    - A dataframe with the normalized marks for the given section.
    """
    # Group by exam_date and calculate necessary statistics
    exam_stats = df.groupby('exam_date')[marks_column].agg(['mean', 'std']).reset_index()
    exam_stats.columns = ['exam_date', f'exam_mean_{section_name}', f'exam_std_{section_name}']
    
    # Calculate top percentile mean (M_ti) for the given section
    M_ti = df.groupby('exam_date')[marks_column].apply(lambda x: x.nlargest(max(1, len(x) // 1000)).mean()).reset_index()
    M_ti.columns = ['exam_date', f'exam_M_ti_{section_name}']
    
    # Overall statistics for the given section
    overall_mean = df[marks_column].mean()
    overall_std_dev = df[marks_column].std()
    
    # Calculate the top percentile mean across all data
    M_tg = df[marks_column].nlargest(max(1, len(df[marks_column]) // 1000)).mean()
    
    # Merge the statistics with the data
    df = df.merge(exam_stats, on='exam_date', how='left').merge(M_ti, on='exam_date', how='left')
    
    # Compute IQ threshold
    df[f'exam_M_iq_{section_name}'] = df[f'exam_mean_{section_name}'] + df[f'exam_std_{section_name}']
    
    # Global IQ mark
    Mg_q = overall_mean + overall_std_dev
    
    # Max-mean based normalization factor
    max_mean_exam = exam_stats.loc[exam_stats[f'exam_mean_{section_name}'].idxmax()]
    Mg_qm = max_mean_exam[f'exam_mean_{section_name}'] + max_mean_exam[f'exam_std_{section_name}']
    
    # Normalize marks
    df[f'normalized_marks_{section_name}'] = ((M_tg - Mg_q) / (df[f'exam_M_ti_{section_name}'] - df[f'exam_M_iq_{section_name}'])) * (df[marks_column] - df[f'exam_M_iq_{section_name}']) + Mg_qm
    
    # Drop unnecessary columns
    df = df.drop(columns=[f'exam_M_ti_{section_name}', f'exam_M_iq_{section_name}', f'exam_mean_{section_name}', f'exam_std_{section_name}'])
    
    return df


# Read data from CSV
df = pd.read_csv('combined_data_with_details_marks.csv')

# Convert exam_date to string to avoid merge issues
df['exam_date'] = df['exam_date'].astype(str)

# Separate rows where exam_date is "ABSENT"
df_absent = df[df['exam_date'] == "ABSENT"].copy()
df_present = df[df['exam_date'] != "ABSENT"].copy()

# Normalize marks for each section
df_present = normalize_marks(df_present, 'section_1_marks_with_bonous', 's1')
df_present = normalize_marks(df_present, 'section_2_marks_with_bonous', 's2')
df_present = normalize_marks(df_present, 'computer_marks_with_bonous', 'comp')

# Append absent rows without normalization
df_absent['normalized_marks_s1'] = None
df_absent['normalized_marks_s2'] = None
df_absent['normalized_marks_comp'] = None

# Combine the data
df_final = pd.concat([df_present, df_absent], ignore_index=True)

# Save processed data to CSV
df_final.to_csv('with_normalized_marks.csv', index=False)
