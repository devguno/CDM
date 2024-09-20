import os
import pandas as pd
from tqdm import tqdm
import shutil  # 파일 이동을 위해 shutil 모듈 사용

# 경로 설정
csv_path = '/workspace/gunoroh/sftp/code/pt_no_person_id.csv'  ##병록번호와 cdm person_id 가 매칭된 csv 파일
file_dir = '/workspace/gunoroh/sftp_share/hourly_summary'                    ## sig, hea, xml 파일이 존재하는 경로
rename_dir = '/workspace/gunoroh/sftp_share/Holter_hourly_summary'              ## person_id 변환 완료된 파일들을 이동시킬 파일경로

#csv_path = 'D:\\pt_no_person_id.csv'  ##병록번호와 cdm person_id 가 매칭된 csv 파일
#file_dir = 'D:\\test'                    ## sig, hea, xml 파일이 존재하는 경로
#rename_dir = 'D:\\test' 


# rename_dir 폴더가 없으면 생성
if not os.path.exists(rename_dir):
    os.makedirs(rename_dir)

# CSV 파일 로드 및 딕셔너리 생성
df = pd.read_csv(csv_path)
pt_no_to_person_id = df.set_index('pt_no')['person_id'].to_dict()

# 파일 리스트 가져오기
files = [f for f in os.listdir(file_dir) if '_' in f]

moved_count = 0

# 파일 이름 변경 및 이동
for file in tqdm(files, desc="Renaming and moving files"):
    try:
        # 파일명에서 마지막 '_' 다음에 있는 번호를 pt_no로 추출
        parts = file.rsplit('_', 1)
        base_name, pt_no_with_extension = parts[0], parts[1]
        
        pt_no, extension = pt_no_with_extension.split('.')  # pt_no와 확장자를 분리
        person_id = pt_no_to_person_id.get(int(pt_no))  # pt_no에 대응하는 person_id 찾기

        if person_id:
            # person_id를 사용해 새로운 파일명 생성
            new_filename = f'{base_name}_{int(person_id)}.{extension}'  

            old_file_path = os.path.join(file_dir, file)
            new_file_path = os.path.join(rename_dir, new_filename)
            
            # 파일 이동
            shutil.move(old_file_path, new_file_path)
            moved_count += 1  
        else:
            # 매칭되는 person_id가 없으면 파일을 원래 폴더에 그대로 둠
            continue

    except ValueError:
        print(f'Error processing file: {file}')

print(f'Task completed. A total of {moved_count} files were renamed and moved to {rename_dir}.')


