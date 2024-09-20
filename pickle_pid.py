import os
import pickle
from glob import glob

# Pickle 파일을 로드하는 함수
def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# Pickle 파일을 저장하는 함수
def save_pickle(data, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

# 경로에 있는 파일들의 PID를 파일명에서 추출하여 변경하는 함수
def update_pid_in_pickle_files(directory):
    pickle_files = glob(os.path.join(directory, '*.pickle'))  # 디렉터리 내의 모든 피클 파일 검색
    print(f"Found {len(pickle_files)} pickle files.")
    
    for file_path in pickle_files:
        try:
            filename = os.path.basename(file_path)  # 파일명 추출
            filename_without_ext = os.path.splitext(filename)[0]  # 확장자 제거 (예: '2057_62_1569558')
            new_pid = filename_without_ext.split('_')[-1]  # 파일명에서 마지막 '_' 뒤의 숫자를 PID로 추출

            # Pickle 파일 로드
            data = load_pickle(file_path)

            # PID 업데이트
            if 'patient_info' in data and isinstance(data['patient_info'], dict):
                data['patient_info']['PID'] = new_pid  # 파일명에서 추출한 PID로 변경
                print(f"Updating PID for {filename}: New PID = {new_pid}")

                # 수정된 데이터를 다시 피클 파일로 저장
                save_pickle(data, file_path)
            else:
                print(f"No 'patient_info' found or not a valid dict in {filename}. Skipping.")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue

if __name__ == '__main__':
    directory = '/workspace/gunoroh/sftp_share/Holter_hourly_summary'  # 피클 파일들이 있는 디렉터리 경로
    #directory = 'D:\\test'  # 피클 파일들이 있는 디렉터리 경로
    update_pid_in_pickle_files(directory)
