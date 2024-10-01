import os
import json
import csv
from tqdm import tqdm

def load_pt_no_person_id_mapping(csv_file):
    mapping = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping[row['pt_no']] = row['person_id']
    return mapping

def process_json_files(json_folder, csv_file, output_folder):
    pt_no_person_id_mapping = load_pt_no_person_id_mapping(csv_file)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
    
    for filename in tqdm(json_files, desc="처리 중인 파일"):
        parts = filename.split('_')
        if len(parts) not in [3, 4]:
            print(f"경고: 파일 이름 형식이 잘못되었습니다 - {filename}")
            continue
        
        if len(parts) == 4:
            foldername, index, pid, hookupdate = parts
        else:
            foldername, pid, hookupdate = parts
            index = None
        
        if pid not in pt_no_person_id_mapping:
            print(f"경고: {pid}에 대한 person_id를 찾을 수 없습니다 - {filename}")
            continue
        
        person_id = pt_no_person_id_mapping[pid]
        
        if index:
            new_filename = f"{foldername}_{index}_{person_id}_{hookupdate}"
        else:
            new_filename = f"{foldername}_{person_id}_{hookupdate}"
        
        input_path = os.path.join(json_folder, filename)
        output_path = os.path.join(output_folder, new_filename)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if "Holter Report" in data and "PatientInfo" in data["Holter Report"]:
            data["Holter Report"]["PatientInfo"]["PID"] = person_id
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    json_folder = r'/workspace/sftp_share/Holter_raw_json'
    csv_file = r'/workspace/sftp/code/pt_no_person_id.csv'
    output_folder = r'/workspace/sftp_share/Holter_json'
    
    process_json_files(json_folder, csv_file, output_folder)
    print("모든 파일 처리가 완료되었습니다.")