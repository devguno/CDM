import os

def extract_first_numbers(directory_path):
    # 디렉토리 내의 모든 .json 파일 가져오기
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    
    # 숫자만 있는 것과 문자+숫자 조합을 분리하여 저장
    pure_numbers = []
    alphanumeric = []
    
    for filename in json_files:
        # '_'로 분할
        parts = filename.split('_')
        # 4부분으로 나누어진 파일만 처리
        if len(parts) == 4:
            first_part = parts[0]
            if first_part.isdigit():
                pure_numbers.append(int(first_part))
            else:
                alphanumeric.append(first_part)
    
    # 각각 정렬하고 중복 제거
    unique_numbers = sorted(list(set(pure_numbers)))
    unique_alphanumeric = sorted(list(set(alphanumeric)))
    
    # 숫자는 문자열로 변환
    result = [str(num) for num in unique_numbers] + unique_alphanumeric
    
    return result

# 사용 예시
directory_path = '/workspace/nas1/Holter_new/Holter_json'
result = extract_first_numbers(directory_path)

# 결과를 [num1, num2, ...] 형식으로 출력
print('[' + ', '.join(result) + ']')