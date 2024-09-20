from glob import glob
import pandas as pd
import numpy as np
import tabula   # tabula 사용 시 JAVA JDK 설치 필수
import PyPDF2
from datetime import datetime, timedelta
from tqdm import tqdm
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import json
import os
import fitz  # PyMuPDF
import re

# 정규표현식을 사용해 패턴에 맞는 값을 추출하는 함수
def extract_match(pattern, text, default_value):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return default_value

# 날짜 형식을 변환하는 함수 ('29-Apr-2016' -> '2016-04-29')
def convert_date_format(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d-%b-%Y')  # '29-Apr-2016' 형식 파싱
        return date_obj.strftime('%Y-%m-%d')  # '2016-04-29' 형식으로 변환
    except ValueError:
        return date_str  # 변환 실패 시 원래 값을 반환

# PDF 파일 불러와서 DataFrame 형태로 변환
def convert_pdf_to_dict(paths, output_path, save=True):
    if not isinstance(paths, list):
            raise TypeError("파일 경로는 리스트 타입이어야 합니다.")
    
    print(f"PDF 파일 {len(paths)}개 변환 시작")
        
    columns = [
        "Hour", "Min", "#QRS's", "Min.", 
        "Ave.", "Max.", "Pauses", "V_Iso", "V_Cplt", "V_Runs", "V_Max_Run", "V_Max_Rate", 
        "S_Iso", "S_Cplt", "S_Runs", "S_Max_Run", "S_Max_Rate"
        ] 
    
    total_dict = {}
    error_files = []
    error_count = 0
    
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

            # 두 번째부터 다섯 번째 페이지까지 데이터 추출
            for page_num in range(1, 6):
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
                except Exception as e:
                    print(f"Error reading page {page_num} of {path}: {str(e)}")
                    continue

                # Hourly Summary 데이터를 변환
                hourly_summary_df = _pdf.iloc[6:-1]
                new_df = pd.DataFrame()
                for col in hourly_summary_df.columns:
                    new_df = pd.concat([new_df, hourly_summary_df[col].str.split(" ", expand=True)], axis=1)
                
                # 결측값 처리
                new_df.replace('---', np.nan, inplace=True)
                new_df.reset_index(drop=True, inplace=True) 
                new_df.columns = columns
                
                # NaN 값을 제외한 모든 값을 정수형으로 변환하는 함수 정의
                def convert_to_int(value):
                    if pd.isna(value): 
                        return value
                    else: 
                        return int(value)
                new_df = new_df.applymap(convert_to_int)
                new_df.fillna(0, inplace=True)
                new_df = new_df.astype(int)
                
                # 제대로 변형 되었는지 검증 (HR #QRS's 비교)
                _sum_str = ' '.join(_pdf.iloc[-1].astype(str))
                _sum_list = [int(value) for value in _sum_str.split()]
                df_sum = new_df["#QRS's"].sum()
                if _sum_list[1] != df_sum:
                    raise Exception(f"Dataframe이 정상적으로 변형되지 않았습니다. 데이터를 확인하세요. PID : {pid} raw_sum : {_sum_list[0]} / df_sum : {df_sum}")
                
                # Hourly Summary Dict로 변환
                _dict = {
                    'PatientInfo': patient_info,
                    'HR': {
                        'Hour': new_df.loc[:, "Hour"].tolist(), 
                        'Min': new_df.loc[:, "Min"].tolist(), 
                        "#QRS's" : new_df.loc[:, "#QRS's"].tolist(),
                        "Min." : new_df.loc[:, "Min."].tolist(),
                        "Ave." : new_df.loc[:, "Ave."].tolist(),
                        "Max." : new_df.loc[:, "Max."].tolist(),
                        "Pauses": new_df.loc[:, "Pauses"].tolist()
                    },
                    'VT': {
                        'Hour' : new_df.loc[:, "Hour"].tolist(), 
                        'Min' : new_df.loc[:, "Min"].tolist(), 
                        'Iso' : new_df.loc[:, "V_Iso"].tolist(),
                        'Cplt' : new_df.loc[:, "V_Cplt"].tolist(),
                        'Runs' : new_df.loc[:, "V_Runs"].tolist(),
                        'Max_Run' : new_df.loc[:, "V_Max_Run"].tolist(),
                        'Max_Rate' : new_df.loc[:, "V_Max_Rate"].tolist()
                    },
                    'SVT': {
                        'Hour' : new_df.loc[:, "Hour"].tolist(), 
                        'Min' : new_df.loc[:, "Min"].tolist(), 
                        'Iso' : new_df.loc[:, "S_Iso"].tolist(),
                        'Cplt' : new_df.loc[:, "S_Cplt"].tolist(),
                        'Runs' : new_df.loc[:, "S_Runs"].tolist(),
                        'Max_Run' : new_df.loc[:, "S_Max_Run"].tolist(),
                        'Max_Rate' : new_df.loc[:, "S_Max_Rate"].tolist()
                    }
                }
                
                # JSON 파일로 저장
                with open(f"{output_path}/{filename_without_ext}.json", 'w') as f:
                    json.dump(_dict, f, indent=4)
                
                total_dict[pid] = _dict
                break
        
        except Exception as e:
            print(f"Error processing file {path}: {str(e)}")
            error_files.append(path)
            error_count += 1
            continue
    
    print(f"{len(total_dict)}개의 Hourly Summary 테이블을 저장했습니다.")
    print(f"에러가 발생한 파일 개수: {error_count}")
    if error_files:
        print("에러가 발생한 파일 목록:")
        for file in error_files:
            print(file)

    return total_dict

if __name__ == '__main__':
    # root_dirs = [
    #     '/workspace/nas1/Holter_new/Holter_raw_sig', 
    #     '/workspace/nas1/Holter/Holter_raw_sig'
    # ]
    # output_dir = '/workspace/gunoroh/sftp_share/hourly_summary' 

    root_dir = 'D:\\extract'
    output_dir = 'D:\\hourly' 
    paths = glob(f"{root_dir}/*.pdf")

    # paths = []
    # for root_dir in root_dirs:
    #     paths.extend(glob(f"{root_dir}/*.pdf"))
    
    total_dict = convert_pdf_to_dict(paths, output_dir)