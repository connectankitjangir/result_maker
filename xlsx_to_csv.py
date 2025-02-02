import pandas as pd

input_file = 'with_normalized_marks_updated.xlsx'
output_file = 'with_normalized_marks_updated.csv'

df = pd.read_excel(input_file)
df.to_csv(output_file, index=False)
