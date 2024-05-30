import os
import re
from collections import defaultdict
from tqdm import tqdm

def find_and_remove_incomplete_files(folder_path):
    # 파일 이름 패턴 정의
    file_pattern = re.compile(r'(\d+)_(\d+)\.(hea|SIG|pdf)')
    
    # 인덱스 번호별 파일 목록 저장
    files_dict = defaultdict(list)
    
    # 폴더 내 파일 검사
    for filename in tqdm(os.listdir(folder_path), desc="Scanning files"):
        match = file_pattern.match(filename)
        if match:
            index_number = match.group(1)
            files_dict[index_number].append(filename)
    
    # 3개의 파일이 없는 인덱스 번호 찾기 및 파일 제거
    incomplete_indices = [index for index, files in files_dict.items() if len(files) != 3]
    for index in tqdm(incomplete_indices, desc="Removing incomplete files"):
        for filename in files_dict[index]:
            os.remove(os.path.join(folder_path, filename))
        del files_dict[index]  # 사전에서 제거
    
    print(f'Removed incomplete index numbers: {incomplete_indices}')
    return files_dict

def rename_files(folder_path, files_dict):
    new_index = 10000
    for index, files in tqdm(sorted(files_dict.items()), desc="Renaming files"):
        for filename in files:
            new_filename = re.sub(r'^\d+', str(new_index), filename)
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
        new_index += 1

def main():
    folder_path = r'Z:\Holter\extract\child_cd'
    files_dict = find_and_remove_incomplete_files(folder_path)
    rename_files(folder_path, files_dict)

if __name__ == "__main__":
    main()
