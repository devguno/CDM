import os
import shutil
import math

def split_folders(base_path):
    # 기본 경로의 모든 폴더 가져오기
    folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        # 폴더 내의 모든 파일 리스트
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        total_files = len(files)
        
        # 필요한 폴더 수 계산 (200개씩)
        num_folders = math.ceil(total_files / 200)
        
        if num_folders > 0:
            # 각 폴더별로 처리
            for i in range(num_folders):
                # 새 폴더 이름 생성
                new_folder_name = f"boramae_{folder}"
                if i > 0:
                    new_folder_name += f"_{i+1}"
                
                # 새 폴더 경로
                new_folder_path = os.path.join(base_path, new_folder_name)
                
                # 새 폴더 생성
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                
                # 이동할 파일 범위 계산
                start_idx = i * 200
                end_idx = min((i + 1) * 200, total_files)
                
                # 파일 이동
                for file_name in files[start_idx:end_idx]:
                    old_path = os.path.join(folder_path, file_name)
                    new_path = os.path.join(new_folder_path, file_name)
                    shutil.move(old_path, new_path)
            
            # 원본 폴더가 비었다면 삭제
            if len(os.listdir(folder_path)) == 0:
                os.rmdir(folder_path)

# 실행
base_path = r"C:\boramae"
split_folders(base_path)

print("폴더 분할이 완료되었습니다.")