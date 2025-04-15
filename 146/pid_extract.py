import os
import json
import csv

# JSON 파일들이 있는 디렉토리
json_dir = r'C:\extract\json'

# PID만 저장할 리스트
pid_list = []

# 디렉토리 내 모든 JSON 파일 반복
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(json_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                pid = data.get("Holter Report", {}).get("PatientInfo", {}).get("PID", "")
                if pid:
                    pid_list.append([pid])  # 리스트 안에 리스트 형태로 저장 (CSV용)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# PID만 CSV로 저장
csv_path = os.path.join(json_dir, 'pid_list.csv')
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['pt_no'])  # 헤더
    writer.writerows(pid_list)

print(f"PID 리스트가 저장되었습니다: {csv_path}")
