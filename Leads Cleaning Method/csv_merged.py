import os
import pandas as pd
from datetime import datetime

def merge_csv_files():
    # Get today's date
    today = datetime.today().strftime('%d-%m-%Y')

    # Define paths
    main_folder = os.path.join(os.getcwd(), today, 'Clean_Leads')
    merged_file_path = os.path.join(main_folder, 'merged.csv')

    # Check if merged file already exists
    if os.path.exists(merged_file_path):
        print("Merged file already exists.")
        return

    # Get list of CSV files in clean_leads folder
    csv_files = [file for file in os.listdir(main_folder) if file.endswith('.csv')]

    # Check if there are CSV files to merge
    if len(csv_files) == 0:
        print("No CSV files found in clean_leads folder.")
        return

    # Merge CSV files
    dfs = []
    total_records_before_merge = 0
    records_per_file = {}

    for file in csv_files:
        file_path = os.path.join(main_folder, file)
        df = pd.read_csv(file_path)
        dfs.append(df)
        records_per_file[file] = len(df)
        total_records_before_merge += len(df)

    merged_df = pd.concat(dfs, ignore_index=True)

    # Write merged DataFrame to a new CSV file
    merged_df.to_csv(merged_file_path, index=False)

    # Get total records after merge
    total_records_after_merge = len(merged_df)

    # Print insights
    print("Merge Insights:")
    print(f"Total CSV files merged: {len(csv_files)}")
    for file, records in records_per_file.items():
        print(f" - {file}: {records} records")
    print(f"Total records before merge: {total_records_before_merge}")
    print(f"Total records after merge: {total_records_after_merge}")
    if total_records_before_merge == total_records_after_merge:
        print("Merge successful.")
    else:
        print("Merge unsuccessful. Number of records mismatch.")

    print(f"Merged file saved at '{merged_file_path}'.")

if __name__ == "__main__":
    merge_csv_files()
