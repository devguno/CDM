import os
import json
import csv
from tqdm import tqdm

# JSON 파일들이 있는 디렉토리
json_dir = r'C:\extract\json'

# 저장할 CSV 파일 경로
csv_path = r'C:\Users\SNUH\OneDrive\SNUH BMI Lab\github\CDM\pid_list.csv'

# PID만 저장할 리스트
pid_list = []

# 디렉토리 내 모든 JSON 파일 목록
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

# tqdm으로 진행상황 표시하며 반복
for filename in tqdm(json_files, desc="Processing JSON files"):
    file_path = os.path.join(json_dir, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            pid = data.get("Holter Report", {}).get("PatientInfo", {}).get("PID", "")
            if pid:
                pid_list.append([pid])
    except Exception as e:
        print(f"Error reading {filename}: {e}")

# PID만 CSV로 저장
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['pt_no'])  # 헤더
    writer.writerows(pid_list)

print(f"\nPID 리스트가 저장되었습니다: {csv_path}")
