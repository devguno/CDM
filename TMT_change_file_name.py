import os
import re

def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".XML"):  # XML 파일인지 확인
            # 정규 표현식으로 파일명에서 영어 이름과 숫자를 분리합니다.
            match = re.search(r'([0-9]+)#([A-Z]+)#([A-Z ]+)([0-9_]+)#([0-9_]+)\.XML', filename)
            if match:
                identifier = match.group(1)
                date = match.group(4)
                time = match.group(5)
                new_filename = f"{identifier}#{date}#{time}.XML"
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                print(f'Renamed {filename} to {new_filename}')

# Replace the path with your directory path
#directory_path = 'Z:/main_tmt/Main TMT Device #2/201904to201905'
directory_path = r'C:\Users\SNUH\Desktop\test'
rename_files(directory_path)

