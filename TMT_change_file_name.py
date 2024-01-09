import os
import re
from tqdm import tqdm

def rename_files(base_directory):
    for dirpath, dirnames, filenames in os.walk(base_directory):
        for filename in tqdm(filenames, desc=f"Processing {dirpath}"):
            if filename.endswith(".XML"):  # XML 파일인지 확인
                # 정규 표현식으로 파일명에서 영어 이름과 숫자를 분리합니다.
                match = re.search(r'([0-9]+)#([A-Z]+)#([A-Z ]+)([0-9_]+)#([0-9_]+)\.XML', filename)
                if match:
                    identifier = match.group(1)
                    date = match.group(4)
                    time = match.group(5)
                    new_filename = f"{identifier}#{date}#{time}.XML"
                    original_file_path = os.path.join(dirpath, filename)
                    new_file_path = os.path.join(dirpath, new_filename)
                    os.rename(original_file_path, new_file_path)
                    print(f'Renamed {filename} to {new_filename}')

# Replace the path with your directory path
#base_directory_path = r'C:\Users\SNUH\Desktop\test'
base_directory_path = 'Z:/main_tmt/Main TMT Device #2'
rename_files(base_directory_path)

