import json
import csv
import glob
import os
from tqdm import tqdm
from datetime import datetime

def flatten_json(nested_json, prefix=''):
    flattened = {}
    
    for key, value in nested_json.items():
        if isinstance(value, dict):
            flattened.update(flatten_json(value, f"{prefix}{key}_"))
        else:
            if value == "Unknown":
                value = ""
            flattened[f"{prefix}{key}"] = value
            
    return flattened

def process_holter_report(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Holter Report 데이터만 추출
    holter_data = data.get('Holter Report', {})
    
    flattened_data = flatten_json(holter_data)
    
    # 파일 경로 추가
    flattened_data['FilePath'] = file_path
    
    # 파일명에서 확장자 제거하여 추가
    filename_without_ext = os.path.splitext(os.path.basename(file_path))[0]
    flattened_data['FileName'] = filename_without_ext
    
    # QRS complexes 기준 백분율 계산
    try:
        qrs_complexes = float(flattened_data.get('General_QRScomplexes', 0))
        if qrs_complexes > 0:
            # Ventricular Beats Percentage 계산
            vent_beats = float(flattened_data.get('General_VentricularBeats', 0))
            flattened_data['VentricularBeatsPercentage'] = round((vent_beats / qrs_complexes) * 100, 2)
            
            # Supraventricular Beats Percentage 계산
            supra_beats = float(flattened_data.get('General_SupraventricularBeats', 0))
            flattened_data['SupraventricularBeatsPercentage'] = round((supra_beats / qrs_complexes) * 100, 2)
        else:
            flattened_data['VentricularBeatsPercentage'] = 0
            flattened_data['SupraventricularBeatsPercentage'] = 0
    except (ValueError, TypeError):
        flattened_data['VentricularBeatsPercentage'] = ''
        flattened_data['SupraventricularBeatsPercentage'] = ''
    
    # HookupDate와 HookupTime 결합하여 새로운 필드 추가
    if 'PatientInfo_HookupDate' in flattened_data and 'PatientInfo_HookupTime' in flattened_data:
        date = flattened_data['PatientInfo_HookupDate']
        time = flattened_data['PatientInfo_HookupTime']
        if date and time:  
            combined_datetime = f"{date} {time}"
            flattened_data['PatientInfo_HookupDateTime'] = combined_datetime
    
    return flattened_data

def main():
    json_dir = '/workspace/nas1/Holter_new/Holter_json'
    output_dir = '/workspace/sftp'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    json_files = glob.glob(os.path.join(json_dir, '*.json'))
    
    if not json_files:
        print("JSON 파일을 찾을 수 없습니다.")
        return
        
    first_data = process_holter_report(json_files[0])
    headers = list(first_data.keys())
    
    # FilePath와 FileName을 마지막 컬럼으로 이동
    for field in ['FilePath', 'FileName']:
        if field in headers:
            headers.remove(field)
            headers.append(field)
    
    output_file = os.path.join(output_dir, 'holter_reports.csv')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        writer.writeheader()
        
        for json_file in tqdm(json_files, desc="파일 처리 중"):
            try:
                data = process_holter_report(json_file)
                writer.writerow(data)
            except Exception as e:
                print(f"\n오류 발생 ({os.path.basename(json_file)}): {str(e)}")
    
    print(f"\n변환 완료! CSV 파일이 저장됨: {output_file}")

if __name__ == '__main__':
    main()