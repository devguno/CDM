import json
import csv
import glob
import os
from tqdm import tqdm
from datetime import datetime

def flatten_json(nested_json, prefix=''):
    """
    중첩된 JSON을 평탄화하여 단일 레벨의 딕셔너리로 변환
    Unknown 값은 빈 문자열로 변환
    """
    flattened = {}
    
    for key, value in nested_json.items():
        if isinstance(value, dict):
            flattened.update(flatten_json(value, f"{prefix}{key}_"))
        else:
            # Unknown 값을 빈 문자열로 변환
            if value == "Unknown":
                value = ""
            flattened[f"{prefix}{key}"] = value
            
    return flattened

def process_holter_report(file_path):
    """
    Holter Report JSON 파일을 처리하여 평탄화된 데이터를 반환
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Holter Report 데이터만 추출
    holter_data = data.get('Holter Report', {})
    
    # JSON 평탄화
    flattened_data = flatten_json(holter_data)
    
    # HookupDate와 HookupTime 결합하여 새로운 필드 추가
    if 'PatientInfo_HookupDate' in flattened_data and 'PatientInfo_HookupTime' in flattened_data:
        date = flattened_data['PatientInfo_HookupDate']
        time = flattened_data['PatientInfo_HookupTime']
        if date and time:  # 둘 다 값이 있는 경우에만 처리
            combined_datetime = f"{date} {time}"
            # 새로운 필드로 추가
            flattened_data['PatientInfo_HookupDateTime'] = combined_datetime
    
    return flattened_data

def main():
    # JSON 파일들이 있는 디렉토리 경로
    #json_dir = r'C:\ttt'
    json_dir = 'C:\\boramae_json'
    # 결과 저장 경로
    #output_dir = r'C:\tt'
    output_dir = 'C:\\finish'

    # output_dir이 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 모든 JSON 파일 경로 가져오기
    json_files = glob.glob(os.path.join(json_dir, '*.json'))
    
    if not json_files:
        print("JSON 파일을 찾을 수 없습니다.")
        return
        
    # 첫 번째 파일을 처리하여 헤더 얻기
    first_data = process_holter_report(json_files[0])
    headers = list(first_data.keys())
    
    # CSV 파일 생성
    output_file = os.path.join(output_dir, 'holter_reports.csv')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # 헤더 작성
        writer.writeheader()
        
        # tqdm으로 진행률 표시하며 모든 JSON 파일 처리
        for json_file in tqdm(json_files, desc="파일 처리 중"):
            try:
                data = process_holter_report(json_file)
                writer.writerow(data)
            except Exception as e:
                print(f"\n오류 발생 ({os.path.basename(json_file)}): {str(e)}")
    
    print(f"\n변환 완료! CSV 파일이 저장됨: {output_file}")

if __name__ == '__main__':
    main()