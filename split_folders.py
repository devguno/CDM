import os
import math
import shutil

# 원본 폴더 경로
source_dir = r'F:\boramae_2010'
# .nat 파일 리스트 가져오기
nat_files = [f for f in os.listdir(source_dir) if f.endswith('.nat')]

# 파일을 190개씩 나눴을 때 필요한 폴더 수 계산
num_folders = math.ceil(len(nat_files) / 190)

# 각 폴더별로 파일 이동
for folder_num in range(num_folders):
    # 새로운 폴더 이름 생성 (boramae_201001, boramae_201002, ...)
    new_folder_name = f'boramae_2010{str(folder_num + 1).zfill(2)}'
    new_folder_path = os.path.join(source_dir, new_folder_name)
    
    # 폴더가 없으면 생성
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    
    # 현재 폴더에 들어갈 파일들의 시작과 끝 인덱스 계산
    start_idx = folder_num * 190
    end_idx = min((folder_num + 1) * 190, len(nat_files))
    
    # 파일 이동
    for file_name in nat_files[start_idx:end_idx]:
        source_file = os.path.join(source_dir, file_name)
        dest_file = os.path.join(new_folder_path, file_name)
        shutil.move(source_file, dest_file)

print('파일 분류가 완료되었습니다.')