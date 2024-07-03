import os
import pandas as pd

# CSV 파일들이 저장된 디렉토리
csv_dir = 'Z:\\Holter'

# CSV 파일 리스트 수집
csv_files = [os.path.join(csv_dir, f) for f in os.listdir(csv_dir) if f.startswith('patient_info_batch_') and f.endswith('.csv')]

# 모든 CSV 파일 병합
df_list = [pd.read_csv(file) for file in csv_files]
df = pd.concat(df_list, ignore_index=True)

# 전체 환자 수 계산
total_patients = df['PID'].nunique()

# HookupDate를 datetime 형식으로 변환
df['HookupDate'] = pd.to_datetime(df['HookupDate'], format='%Y%m%d')

# 동일한 PID를 가진 환자의 HookupDate 차이 계산
df_sorted = df.sort_values(by=['PID', 'HookupDate'])
df_sorted['NextHookupDate'] = df_sorted.groupby('PID')['HookupDate'].shift(-1)
df_sorted['DaysBetween'] = (df_sorted['NextHookupDate'] - df_sorted['HookupDate']).dt.days

# 두 번 이상 측정한 환자 수 계산
multiple_measurements = df_sorted['PID'].value_counts()
num_patients_multiple_measurements = (multiple_measurements > 1).sum()

# HookupDate 간격 통계
days_between_stats = df_sorted['DaysBetween'].dropna().describe()

# 결과 출력
print(f"전체 환자 수: {total_patients}")
print(f"두 번 이상 측정한 환자 수: {num_patients_multiple_measurements}")
print("HookupDate 간격 통계:")
print(days_between_stats)

# 결과 저장 (원하는 경우 CSV 파일로 저장)
output_csv_path = os.path.join(csv_dir, 'days_between_measurements.csv')
df_sorted.to_csv(output_csv_path, index=False)
