import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

def remove_data_from_xml(file_path, output_path):
    try:
        # XML 파일을 파싱합니다
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 지정된 태그들을 찾아 데이터를 삭제합니다
        tags_to_remove = ['birthdate', 'firstname', 'lastname']
        for tag in tags_to_remove:
            for element in root.iter(tag):
                element.text = None  # 태그 내용을 삭제

        # 수정된 파일을 저장합니다
        tree.write(output_path)
    except Exception as e:
        # 오류 발생 시 파일명과 오류 메시지를 출력합니다
        print(f"Error processing file {file_path}: {e}")

# 원본 파일들이 있는 경로
source_directory = 'Z:\\abr\\abr_xml'
# 출력할 파일들을 저장할 경로
output_directory = 'C:\\Users\\SNUH\\Desktop\\abr\\output'

# source_directory에 있는 모든 폴더와 파일을 탐색합니다
for folder_name, subfolders, filenames in os.walk(source_directory):
    for filename in tqdm(filenames, desc=f"Processing {folder_name}"):
        if filename.endswith('.xml'):
            try:
                # 원본 파일의 전체 경로
                file_path = os.path.join(folder_name, filename)
                # 출력 폴더 경로 (원본 폴더명을 사용)
                output_folder = os.path.join(output_directory, os.path.basename(folder_name))
                # 출력 폴더가 없으면 생성
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                # 출력 파일의 전체 경로
                output_path = os.path.join(output_folder, filename)
                # XML 파일 수정 함수 호출
                remove_data_from_xml(file_path, output_path)
            except Exception as e:
                # 오류 발생 시 파일명과 오류 메시지를 출력합니다
                print(f"Error processing file {file_path}: {e}")
