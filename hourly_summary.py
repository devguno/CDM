import re
from glob import glob
import pandas as pd
import os
import numpy as np
import tabula   # tabula 사용 시 JAVA JDK 설치 필수
import PyPDF2
from datetime import datetime, timedelta
import pickle
from tqdm import tqdm
import xml.etree.ElementTree as ET
import fitz  # PyMuPDF


# 정규표현식을 사용해 패턴에 맞는 값을 추출하는 함수
def extract_match(pattern, text, default_value):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return default_value

# Pickle 파일 저장 함수
def save_pickle(data, path):
    with open(path, 'wb') as fw:
        pickle.dump(data, fw)

# 날짜 형식을 변환하는 함수 ('29-Apr-2016' -> '2016-04-29')
def convert_date_format(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d-%b-%Y')  # '29-Apr-2016' 형식 파싱
        return date_obj.strftime('%Y-%m-%d')  # '2016-04-29' 형식으로 변환
    except ValueError:
        return date_str  # 변환 실패 시 원래 값을 반환
    
# PDF 파일 불러와서 필요한 데이터만 변환
def convert_pdf_to_dict(paths, output_path):
    if not isinstance(paths, list):
        raise TypeError("파일 경로는 리스트 타입이어야 합니다.")
    
    print(f"PDF 파일 {len(paths)}개 변환 시작")
    
    error_files = []  # 에러 발생 파일들을 저장하는 리스트
    all_data = []  # 모든 결과를 저장할 리스트
    
    columns = [
        "Hour", "Min", "#QRS's", "Min.", 
        "Ave.", "Max.", "Pauses", "V_Iso", "V_Cplt", "V_Runs", "V_Max_Run", "V_Max_Rate", 
        "S_Iso", "S_Cplt", "S_Runs", "S_Max_Run", "S_Max_Rate"
    ] 
    
    for path in tqdm(paths):
        try:
            # 파일명에서 PID 추출
            filename = os.path.basename(path)
            filename_without_ext = os.path.splitext(filename)[0]  # 확장자(.pdf)를 제거한 파일명
            pid = filename_without_ext.split('_')[-1]  # 파일명에서 마지막 '_' 뒤의 숫자를 PID로 추출

            # 첫 페이지에서 텍스트 추출 (fitz 사용)
            pdf_doc = fitz.open(path)
            page = pdf_doc.load_page(0)  # 첫 번째 페이지만 로드
            extracted_text = page.get_text()  # 첫 페이지의 텍스트 추출

            # Patient Information 추출 및 날짜 형식 변환
            raw_hookup_date = extract_match(r"Medications:?\n(\d+-\w+-\d+)\nHookup Date:?", extracted_text, "Unknown")
            hookup_date = convert_date_format(raw_hookup_date)  # 날짜 형식 변환

            patient_info = {
                'PID': pid,  # 파일명에서 추출한 PID
                'HookupDate': hookup_date,  # 변환된 날짜를 사용
                'HookupTime': extract_match(r"Hookup Date:?\n(\d+:\d+:\d+)\nHookup Time:?", extracted_text, "Unknown"),
            }

            # Hourly Summary 부분 변환 (페이지 1-4)
            for page_num in range(1, 5):
                try:
                    _pdf = tabula.read_pdf(path, pages=page_num)
                    if len(_pdf) > 0:
                        _pdf = _pdf[0].astype(str)
                        if not _pdf.isin(["Hourly Summary"]).any().any():
                            continue
                    else:
                        continue
                except IndexError:
                    break

                hourly_summary_df = _pdf.iloc[6:-1]

                # 완전한 Hourly Summary Dataframe으로 변형
                new_df = pd.DataFrame()
                for col in hourly_summary_df.columns:
                    new_df = pd.concat([new_df, hourly_summary_df[col].str.split(" ", expand=True)], axis=1)

                # TODO : 결측값 처리 0 or NaN
                new_df.replace('---', np.nan, inplace=True)
                new_df.reset_index(drop=True, inplace=True) 
                new_df.columns = columns

                # NaN 값을 제외한 모든 값을 정수형으로 변환하는 함수 정의
                def convert_to_int(value):
                    if pd.isna(value): return value
                    else: return int(value)

                # 각 열에 대해 apply 사용하여 변환 함수 적용
                new_df = new_df.apply(lambda col: col.map(convert_to_int))

                # Hourly Summary Dict로 변형
                summary = {
                    'HR': pd.concat([new_df.loc[:, "Hour":"Min"], new_df.loc[:, "#QRS's":"Pauses"]], axis=1),
                    'VT': pd.concat([new_df.loc[:, "Hour":"Min"], new_df.loc[:, "V_Iso":"V_Max_Rate"]], axis=1),
                    'SVT': pd.concat([new_df.loc[:, "Hour":"Min"], new_df.loc[:, "S_Iso":"S_Max_Rate"]], axis=1),
                }

                # 필요한 정보 저장
                result = {'patient_info': patient_info, 'summary': summary}
                all_data.append(result)  # 리스트에 추가
                break
        
        except Exception as e:
            # 에러 발생 시 파일명을 출력하고 error_files 리스트에 추가
            print(f"Error processing file: {filename}. Skipping to next file.")
            print(f"Error message: {e}")
            error_files.append(filename)
            continue

    # 모든 데이터를 하나의 pickle 파일로 저장
    save_pickle(all_data, f"{output_path}/all_data.pickle")
    
    # 에러가 발생한 파일 갯수와 파일 목록 출력
    print(f"\nNumber of files with errors: {len(error_files)}")
    if len(error_files) > 0:
        print("Files with errors:")
        for file in error_files:
            print(file)

if __name__ == '__main__':
    root_dir = r'C:\extract'
    output_dir = r'C:\extract' 
    paths = glob(f"{root_dir}/*.pdf")
    
    # PDF 파일을 변환하고 새로운 경로에 저장
    convert_pdf_to_dict(paths, output_dir)

