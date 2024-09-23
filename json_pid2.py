import os
import json

# Folder path where the JSON files are located
json_folder = '/workspace/gunoroh/sftp_share/Holter_hourly_summary'

# Iterate over all JSON files in the json_folder
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        # Full path to the current JSON file
        file_path = os.path.join(json_folder, filename)
        
        # Extract the PID from the filename (after the last '_')
        file_pid = filename.rsplit('_', 1)[-1].split('.')[0]

        # Open and read the JSON file
        with open(file_path, 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)

                # Check if the 'PatientInfo' section and 'PID' exist in the JSON
                if "PatientInfo" in data and "PID" in data["PatientInfo"]:
                    # Update the PID in the JSON file with the PID from the filename
                    data["PatientInfo"]["PID"] = file_pid

                    # Move the file pointer to the beginning and overwrite the file with the updated content
                    f.seek(0)
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    f.truncate()  # Truncate the file to remove any leftover content from the original file

                    print(f'Updated PID in {filename}')
                else:
                    print(f'"PatientInfo" or "PID" not found in {filename}')
            except json.JSONDecodeError:
                print(f'Error reading {filename}, skipping.')
