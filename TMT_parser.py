import os
import csv
import xml.etree.ElementTree as ET
from tqdm import tqdm

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extracting ObservationDateTime
        observation_date_time = root.find('ObservationDateTime')
        date_str = '-'.join([observation_date_time.find(tag).text.zfill(2) for tag in ['Year', 'Month', 'Day']])
        time_str = ':'.join([observation_date_time.find(tag).text.zfill(2) for tag in ['Hour', 'Minute', 'Second']])
        datetime_str = f"{date_str} {time_str}"

        # Extracting PID, FamilyName, and GivenName
        patient_info = root.find('PatientInfo')
        pid = patient_info.find('PID').text
        family_name = patient_info.find('Name/FamilyName').text
        
        # GivenName이 없는 경우를 처리
        given_name_element = patient_info.find('Name/GivenName')
        given_name = given_name_element.text if given_name_element is not None else ""
        
        # Extracting BirthDateTime
        birth_date_time = root.find('.//BirthDateTime')
        birth_year = birth_date_time.find('Year').text
        birth_month = birth_date_time.find('Month').text.zfill(2)
        birth_day = birth_date_time.find('Day').text.zfill(2)
        birthdate_str = f"{birth_year}{birth_month}{birth_day}"

        # Extracting Gender
        gender = root.find('.//Gender').text

        return file_path, pid, family_name, given_name, birthdate_str, gender, date_str, datetime_str
    except ET.ParseError as e:
        print(f"XML Parse Error in file: {file_path}")
    except OSError as e:
        print(f"OS Error in file: {file_path}")
    except Exception as e:
        print(f"Unexpected error in file: {file_path}, Error: {e}")
    return None

# 'Z:\child_tmt\Child TMT Device #1' 폴더
root_directory = 'Z:\gangnam_tmt'
# 결과를 저장할 기본 경로
base_output_directory = 'C:/Users/SNUH/Desktop/tmt/'

# root_directory의 마지막 부분을 폴더 이름으로 사용
output_subfolder_name = os.path.basename(root_directory)
output_directory = os.path.join(base_output_directory, output_subfolder_name)

# 출력 디렉토리가 존재하지 않으면 생성
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for subdir, _, files in tqdm(os.walk(root_directory), desc="Processing folders"):
    if subdir == root_directory:
        continue

    csv_file_path = os.path.join(output_directory, os.path.basename(subdir) + '_data.csv')
    
    # 각 하위 폴더의 XML 파일을 순회하면서 처리하고 CSV 파일에 쓰기
    for filename in tqdm([f for f in files if f.lower().endswith('.xml')], desc=f"Processing XML files in {os.path.basename(subdir)}"):
        file_path = os.path.join(subdir, filename)
        data = parse_xml(file_path)

        # 각 파일 처리 후 CSV 파일에 결과 추가
        if data:
            with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if os.path.getsize(csv_file_path) == 0:
                    # 파일이 비어있다면 헤더 작성
                    writer.writerow(['FilePath', 'PID', 'FamilyName', 'GivenName', 'BirthDate', 'Gender', 'Date', 'DateTime'])
                writer.writerow(data)
