import os
import pandas as pd

# Get the directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Loop through all CSV files in the directory
for file_name in os.listdir(current_dir):
    if file_name.endswith('.csv'):  # Process only CSV files
        file_path = os.path.join(current_dir, file_name)
        
        df = pd.read_csv(file_path)
        
        # Identify columns to drop (3rd and 4th columns are at index 2 and 3)
        columns_to_drop = [df.columns[2], df.columns[3]]
        
        # Drop the specified columns
        df = df.drop(columns=columns_to_drop)
        
        # Save the modified DataFrame back to the same file
        df.to_csv(file_path, header=False, index=False)
        print(f"Processed and saved {file_name}")
