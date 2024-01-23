import os
import pandas as pd
from tqdm import tqdm
import glob

# Function to update the contents of the text file with UTF-16 encoding
def update_text_file_utf16(file_path, new_file_name, new_patient_id):
    with open(file_path, 'r', encoding='utf-16') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        if 'Export File =' in line:
            updated_lines.append(f'Export File = {new_file_name}\n')
        elif 'Patient ID=' in line:
            updated_lines.append(f'Patient ID={new_patient_id}\n')
        elif 'Family Name=' in line:
            continue  # Skip this line to remove it
        else:
            updated_lines.append(line)

    with open(file_path, 'w', encoding='utf-16') as file:
        file.writelines(updated_lines)

# Root directory path to be processed
root_directory_path = r'Z:\emr_origin'

# Output root directory
output_root_directory = r'Z:\emr'

# Load the personid.csv file
personid_df = pd.read_csv(r'C:\Users\SNUH\Desktop\personid.csv')

# Process each year folder
for year_folder in os.listdir(root_directory_path):
    year_path = os.path.join(root_directory_path, year_folder)
    
    # Check if it's a directory and contains the year
    if os.path.isdir(year_path) and year_folder.isdigit():
        # Create output directory for the year if it doesn't exist
        output_year_directory = os.path.join(output_root_directory, year_folder)
        if not os.path.exists(output_year_directory):
            os.makedirs(output_year_directory)

        # Get list of all .txt files in the year directory
        txt_files = glob.glob(f'{year_path}/*.txt')

        # Process each file
        for file_path in tqdm(txt_files, desc=f"Processing files in {year_folder}"):
            try:
                # Extract hospital_person_id from the file name
                hospital_person_id = int(os.path.basename(file_path).split(' - ')[0])

                # Find the corresponding cdm_person_id in the DataFrame
                if hospital_person_id in personid_df['hospital_person_id'].values:
                    cdm_person_id = personid_df.loc[personid_df['hospital_person_id'] == hospital_person_id, 'cdm_person_id'].values[0]
                    
                    # Generate the new file name
                    new_file_name = os.path.basename(file_path).replace(str(hospital_person_id), str(cdm_person_id))
                    new_file_path = os.path.join(output_year_directory, new_file_name)
                    
                    # Update the file contents
                    update_text_file_utf16(file_path, new_file_name, cdm_person_id)

                    # Move the updated file to the output directory
                    os.rename(file_path, new_file_path)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

print("All files processed and moved to the output directories.")