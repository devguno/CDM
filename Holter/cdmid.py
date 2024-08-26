import os
import pandas as pd
from tqdm import tqdm
import shutil  # 파일 복사를 위해 shutil 모듈 사용

# 경로 설정
csv_path = r'/home/gunoroh/sftp/holter_pid.csv'
file_dir =  r'/home/gunoroh/sftp/old_sig'
rename_dir = r'/home/gunoroh/sftp/old_sig_cdmid'

# old_rename 폴더가 없으면 생성
if not os.path.exists(rename_dir):
    os.makedirs(rename_dir)

# CSV 파일 로드 및 딕셔너리 생성
df = pd.read_csv(csv_path)
pid_to_cdm_id = df.set_index('pid')['cdm_id'].to_dict()

# 파일 리스트 가져오기
files = [f for f in os.listdir(file_dir) if '_' in f]

converted_count = 0

# 파일 이름 변경 및 복사
for file in tqdm(files, desc="Renaming files"):
    try:
        parts = file.split('_')
        index_number, pid = parts[0], parts[1].split('.')[0]  # 파일명에서 인덱스 번호와 pid 추출
        extension = parts[1].split('.')[1]  # 파일 확장자 추출
        cdm_id = pid_to_cdm_id.get(int(pid))  # pid에 대응하는 cdm_id 찾기

        if cdm_id:
            # cdm_id를 사용해 새로운 파일명 생성
            new_filename = f'{index_number}_{int(cdm_id)}.{extension}'  

            old_file_path = os.path.join(file_dir, file)
            new_file_path = os.path.join(rename_dir, new_filename)
            # 파일 복사
            shutil.copy(old_file_path, new_file_path)
            converted_count += 1  
    except ValueError:
        print(f'Error processing file: {file}')

print(f'Task completed. A total of {converted_count} files were converted and copied to {rename_dir}.')
