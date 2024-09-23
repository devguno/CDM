import os
import pandas as pd
from tqdm import tqdm
import shutil  # 파일 이동을 위해 shutil 모듈 사용

# 경로 설정
csv_path = r'C:\Users\SNUH\OneDrive\SNUH BMI Lab\CDM\Holter\pid\pt_no_person_id.csv'  ## 병록번호와 cdm person_id가 매칭된 csv 파일
file_dir = r'C:\extract_pc2'         ## sig, hea, xml 파일이 존재하는 경로
rename_dir = r'C:\Holter_sig'           ## .sig, .hea 파일 이동 경로
xml_dir = r'C:\Holter_xml'              ## .xml 파일 이동 경로

# rename_dir 폴더가 없으면 생성
if not os.path.exists(rename_dir):
    os.makedirs(rename_dir)

# xml_dir 폴더가 없으면 생성
if not os.path.exists(xml_dir):
    os.makedirs(xml_dir)

# CSV 파일 로드 및 딕셔너리 생성
df = pd.read_csv(csv_path)
pt_no_to_person_id = df.set_index('pt_no')['person_id'].to_dict()

# 파일 리스트 가져오기 (pdf 파일 제외)
files = [f for f in os.listdir(file_dir) if '_' in f and not f.endswith('.pdf')]

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
            
            # 파일 확장자에 따라 이동 경로 결정
            if extension == 'SIG' or extension == 'hea':
                new_file_path = os.path.join(rename_dir, new_filename)
            elif extension == 'xml':
                new_file_path = os.path.join(xml_dir, new_filename)
            else:
                continue  # .sig, .hea, .xml 외의 파일은 무시

            # 파일 이동
            shutil.move(old_file_path, new_file_path)
            moved_count += 1  
        else:
            # 매칭되는 person_id가 없으면 파일을 원래 폴더에 그대로 둠
            continue

    except ValueError:
        print(f'Error processing file: {file}')

print(f'Task completed. A total of {moved_count} files were renamed and moved.')
