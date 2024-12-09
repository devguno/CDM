import os
import csv
import json
import shutil
from tqdm import tqdm

#csv_path = r'/workspace/sftp/code/pt_no_person_id.csv'
#raw_sig_dir = r'/workspace/sftp/Holter_raw_sig'
#sig_dir = r'/workspace/sftp_share/Holter_sig'
#raw_json_dir = r'/workspace/sftp_share/Holter_raw_json'
#json_dir = r'/workspace/sftp_share/Holter_json'

csv_path = r'C:\Users\SNUH\Documents\github\CDM\pt_no_person_id.csv'
raw_sig_dir = r'D:\exx'
sig_dir = r'D:\child_cdm'
raw_json_dir = r'D:\json'
json_dir = r'D:\child_cdm'

def load_pt_no_person_id_mapping(csv_path):
    mapping = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping[row['pt_no']] = row['person_id']
    return mapping

def process_sig_hea_files(raw_dir, output_dir, mapping):
    for filename in tqdm(os.listdir(raw_dir), desc="Processing SIG/HEA/ANN files"):
        if filename.endswith(('.SIG', '.hea', '.ANN')):
            parts = filename.rsplit('_', 2)
            if len(parts) == 3:
                foldername, index, pt_no = parts
                pt_no = pt_no.split('.')[0]
                
                if pt_no in mapping:
                    person_id = mapping[pt_no]
                    new_filename = f"{foldername}_{index}_{person_id}{os.path.splitext(filename)[1]}"
                    
                    src_path = os.path.join(raw_dir, filename)
                    dst_path = os.path.join(output_dir, new_filename)
                    
                    shutil.copy2(src_path, dst_path)
                    
                    if filename.endswith('.hea'):
                        try:
                            process_hea_file(dst_path)
                        except UnicodeDecodeError:
                            print(f"Error processing file: {dst_path}")
                else:
                    print(f"Skipping SIG/HEA file with no matching person_id: {filename}")
            else:
                print(f"Skipping file with unexpected format: {filename}")

def process_hea_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file {file_path} using UTF-8 encoding.")
        return
    
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    lines[0] = f"{base_filename} {' '.join(lines[0].split()[1:])}\n"
    
    for i in range(1, len(lines)):
        parts = lines[i].split()
        parts[0] = f"{base_filename}.SIG"
        lines[i] = ' '.join(parts) + '\n'
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def process_json_files(raw_dir, output_dir, mapping):
    for filename in tqdm(os.listdir(raw_dir), desc="Processing JSON files"):
        if filename.endswith('.json'):
            parts = filename.rsplit('_', 3)
            if len(parts) == 4:
                foldername, index, pt_no, hookupdate = parts
                
                if pt_no in mapping:
                    person_id = mapping[pt_no]
                    new_filename = f"{foldername}_{index}_{person_id}_{hookupdate}"
                    
                    input_path = os.path.join(raw_dir, filename)
                    output_path = os.path.join(output_dir, new_filename)
                    
                    with open(input_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if "Holter Report" in data and "PatientInfo" in data["Holter Report"]:
                        data["Holter Report"]["PatientInfo"]["PID"] = person_id
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                else:
                    print(f"Skipping JSON file with no matching person_id: {filename}")
            else:
                print(f"Skipping JSON file with unexpected format: {filename}")

def main():
    mapping = load_pt_no_person_id_mapping(csv_path)
    
    os.makedirs(sig_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)
    
    process_sig_hea_files(raw_sig_dir, sig_dir, mapping)
    process_json_files(raw_json_dir, json_dir, mapping)

if __name__ == "__main__":
    main()