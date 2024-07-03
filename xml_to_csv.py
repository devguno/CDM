import os
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm

# XML 파일들이 저장된 디렉토리
xml_dir = 'Z:\\Holter\\xml'
# CSV 파일이 저장될 경로
csv_path = 'Z:\\Holter\\patient_info.csv'

# 데이터를 저장할 리스트 초기화
data = []

# 디렉토리 내 모든 XML 파일 리스트화
xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]

# tqdm을 사용하여 파일 처리 진행 상황 표시
for filename in tqdm(xml_files, desc="Processing XML files"):
    file_path = os.path.join(xml_dir, filename)
    
    try:
        # XML 파일 파싱
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 필요한 정보 추출
        pid = root.find('.//PID').text
        hookup_date = root.find('.//HookupDate').text
        hookup_time = root.find('.//HookupTime').text
        
        # HookupDate 형식 변환 (02-Aug-2022 -> 20220802)
        hookup_date_formatted = pd.to_datetime(hookup_date, format='%d-%b-%Y').strftime('%Y%m%d')
        
        # 데이터를 리스트에 추가 (파일명 포함)
        data.append([pid, hookup_date_formatted, hookup_time, filename])
    except Exception as e:
        print(f"Error processing file {filename}: {e}")
        continue

# DataFrame 생성
df = pd.DataFrame(data, columns=['PID', 'HookupDate', 'HookupTime', 'Filename'])

# HookupDate를 datetime 형식으로 변환
df['HookupDate'] = pd.to_datetime(df['HookupDate'], format='%Y%m%d')

# HookupTime을 datetime 형식으로 변환
df['HookupTime'] = pd.to_datetime(df['HookupTime'], format='%H:%M:%S').dt.time

# HookupDate와 HookupTime을 합쳐서 새로운 datetime 형식으로 변환
df['HookupDateTime'] = df.apply(lambda row: pd.Timestamp.combine(row['HookupDate'], row['HookupTime']), axis=1)

# 원하는 형식으로 변환
df['HookupDate'] = df['HookupDate'].dt.strftime('%Y-%m-%d')
df['HookupDateTime'] = df['HookupDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S.000')

# 원래 HookupTime 열은 제거
df = df.drop(columns=['HookupTime'])

# 컬럼 순서 변경
df = df[['PID', 'HookupDate', 'HookupDateTime', 'Filename']]

# CSV 파일로 저장
df.to_csv(csv_path, index=False)

# 결과 출력
print(df.head())
