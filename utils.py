from glob import glob
import pandas as pd
import numpy as np
import tabula   # tabula 사용 시 JAVA JDK 설치 필수
import PyPDF2
from datetime import datetime, timedelta
import pickle
from tqdm import tqdm
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import json
import os


# Dict 데이터 Pickle 저장
def save_pickle(data, path):
    with open(path,'wb') as fw:
        pickle.dump(data, fw)

def load_pickle(path):
    with open(path, 'rb') as fr:
        return pickle.load(fr)

# def detect_target_page(path):
#     process_pdf_files(base_dirs, xml_dir)
    


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
    for path in tqdm(paths):
        file_name = os.path.splitext(os.path.basename(path))[0]
        for page in range(1,6):
            
            try:
                _pdf = tabula.read_pdf(path, pages=page)
                if len(_pdf) > 0:
                    _pdf = _pdf[0].astype(str)
                    if not _pdf.isin(["Hourly Summary"]).any().any():
                        continue
                else:
                    continue
            except IndexError:
                break
            except:
                continue
                
            
            pid = _pdf.columns[0].replace(" ", "").split(":")[1]
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
            new_df = new_df.applymap(convert_to_int)
            new_df.fillna(0,inplace=True)
            new_df = new_df.astype(int)
            
            # 제대로 변형 되었는지 검증 (HR #QRS's 비교)
            _sum_str = ' '.join(_pdf.iloc[-1].astype(str))
            _sum_list = [int(value) for value in _sum_str.split()]
            df_sum = new_df["#QRS's"].sum()
            if _sum_list[1] != df_sum:
                raise Exception(f"Dataframe이 정상적으로 변형되지 않았습니다. 데이터를 확인하세요. PID : {pid} raw_sum : {_sum_list[0]} / df_sum : {df_sum}")
            
            # Hourly Summary Dict로 변형
            _dict = {}
            _dict['HR'] = {
                'Hour': new_df.loc[:, "Hour"].tolist(), 
                'Min': new_df.loc[:, "Min"].tolist(), 
                "#QRS's" : new_df.loc[:, "#QRS's"].tolist(),
                "Min." : new_df.loc[:, "Min."].tolist(),
                "Ave." : new_df.loc[:, "Ave."].tolist(),
                "Max." : new_df.loc[:, "Max."].tolist(),
                "Pauses": new_df.loc[:, "Pauses"].tolist()
            }
            
            _dict['VT'] = {
                'Hour' : new_df.loc[:, "Hour"].tolist(), 
                'Min' : new_df.loc[:, "Min"].tolist(), 
                'Iso' : new_df.loc[:, "V_Iso"].tolist(),
                'Cplt' : new_df.loc[:, "V_Cplt"].tolist(),
                'Runs' : new_df.loc[:, "V_Runs"].tolist(),
                'Max_Run' : new_df.loc[:, "V_Max_Run"].tolist(),
                'Max_Rate' : new_df.loc[:, "V_Max_Rate"].tolist()
            }
            
            _dict['SVT'] = {
                'Hour' : new_df.loc[:, "Hour"].tolist(), 
                'Min' : new_df.loc[:, "Min"].tolist(), 
                'Iso' : new_df.loc[:, "S_Iso"].tolist(),
                'Cplt' : new_df.loc[:, "S_Cplt"].tolist(),
                'Runs' : new_df.loc[:, "S_Runs"].tolist(),
                'Max_Run' : new_df.loc[:, "S_Max_Run"].tolist(),
                'Max_Rate' : new_df.loc[:, "S_Max_Rate"].tolist()
            }
            
            with open(f"{output_path}/{file_name}.json", 'w') as f:
                json.dump(_dict, f, indent=4)
            
            total_dict[pid] = _dict
            
            break
    
    print(f"{len(total_dict)}개의 Hourly Summary 테이블을 저장했습니다.")

    return total_dict


if __name__ == '__main__':
    root_dir = '/workspace/nas1/Holter_new/Holter_raw_sig'
    output_dir = '/workspace/gunoroh/sftp_share/hourly_summary' 
    paths = glob(f"{root_dir}/*.pdf")
    total_dict = convert_pdf_to_dict(paths, output_dir)