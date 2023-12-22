import pandas as pd
import re
from datetime import datetime

# 파일 로드
file_path = 'D:/OneDrive/SNUH BMI Lab/소아CDM/EMG/metadata_file.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path, encoding='cp949')

# 'Export File' 컬럼에서 날짜와 시간 정보 추출
def extract_datetime(text):
    # '-'로 구분된 두 번째 부분 찾기
    parts = text.split(' - ')
    if len(parts) >= 2:
        date_time_str = parts[1]
        # 날짜 형식 변환 (예: '8_10_2010 2_22_37 PM' -> '2010-08-10 14:22:37')
        date_time_str = re.sub(r'(\d+)_(\d+)_(\d+)\s+(\d+_\d+_\d+)\s+(AM|PM)', r'\3-\1-\2 \4 \5', date_time_str)
        # datetime 객체로 변환
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %I_%M_%S %p')
        return date_time_obj
    else:
        return None

# 새 컬럼 생성
df['bio_signal_datetime'] = df['Export File'].apply(lambda x: extract_datetime(x))
df['bio_signal_date'] = df['bio_signal_datetime'].dt.date

# 결과 확인
print(df.head())

# 새로운 파일로 저장 (사용자가 원하는 경로와 파일 이름으로 변경 필요)
output_file_path = 'D:/OneDrive/SNUH BMI Lab/소아CDM/EMG/updated_metadata_file.csv'
df.to_csv(output_file_path, index=False)

output_file_path
