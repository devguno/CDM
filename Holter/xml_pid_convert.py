import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

# 폴더 경로
folder_path = r'C:\Holter_xml'

# 폴더 내의 모든 XML 파일을 확인
xml_files = [file for file in os.listdir(folder_path) if file.endswith('.xml')]

# tqdm을 사용하여 진행 상황 표시
for file_name in tqdm(xml_files, desc="Processing XML files"):
    file_path = os.path.join(folder_path, file_name)
    
    try:
        # 파일명에서 '_' 뒤의 값을 추출
        new_pid = file_name.split('_')[-1].split('.')[0]
        
        # XML 파일 로드
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # PID 태그를 찾고 값을 새로운 PID로 변경
        for pid in root.iter('PID'):
            pid.text = new_pid
        
        # 변경된 XML을 파일에 다시 저장
        tree.write(file_path)
    
    except ET.ParseError:
        print(f"ParseError: Unable to process {file_name}. The file may be malformed.")
    except Exception as e:
        print(f"An error occurred while processing {file_name}: {e}")

print("모든 XML 파일의 PID 값이 변경되었습니다.")
