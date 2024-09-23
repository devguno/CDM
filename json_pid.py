import os
import shutil
import pandas as pd

# File paths
json_folder = '/workspace/gunoroh/sftp_share/hourly_summary'
csv_file = '/workspace/gunoroh/sftp/code/pt_no_person_id.csv'
output_folder = '/workspace/gunoroh/sftp_share/Holter_hourly_summary'

# Load the CSV file containing pt_no and person_id mapping
df = pd.read_csv(csv_file)

# Create a dictionary for fast lookup
pt_to_person_id = dict(zip(df['pt_no'].astype(str), df['person_id'].astype(str)))

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate over all JSON files in the json_folder
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        # Extract pt_no from the filename (after the last '_')
        pt_no = filename.rsplit('_', 1)[-1].split('.')[0]

        # Check if the pt_no exists in the dictionary
        if pt_no in pt_to_person_id:
            person_id = pt_to_person_id[pt_no]

            # Create the new filename by replacing pt_no with person_id
            new_filename = filename.replace(f'_{pt_no}', f'_{person_id}')

            # Full paths for source and destination
            src_path = os.path.join(json_folder, filename)
            dest_path = os.path.join(output_folder, new_filename)

            # Copy the file to the destination with the new filename
            shutil.copy(src_path, dest_path)
            print(f'Copied: {filename} -> {new_filename}')
        else:
            print(f'No match found for pt_no: {pt_no}')
