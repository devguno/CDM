import os

def extract_first_numbers(directory_path):
    # 디렉토리 내의 모든 .json 파일 가져오기
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    
    # 각 파일명에서 첫 번째 숫자 추출 (4부분으로 나누어진 파일만)
    first_numbers = []
    for filename in json_files:
        # '_'로 분할
        parts = filename.split('_')
        # 4부분으로 나누어진 파일만 처리
        if len(parts) == 4:
            first_numbers.append(parts[0])
    
    # 중복 제거 및 정렬
    unique_numbers = sorted(list(set(first_numbers)))
    
    return unique_numbers

# 사용 예시
directory_path = '/workspace/nas1/Holter_new/Holter_json'
result = extract_first_numbers(directory_path)

# 결과 출력
print("추출된 번호:")
for number in result:
    print(number)