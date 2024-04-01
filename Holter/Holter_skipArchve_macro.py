import os
import pyautogui
import pyperclip
import time
import keyboard
from tqdm import tqdm
import math

# 지정된 디렉토리 설정
directory = "Z:\\Holter\\Holter_child_hdd\\2022"

# # 디렉토리 내의 모든 하위 폴더명을 리스트로 가져오기
#folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
#print(f"folder list: {folder_list}")  
folder_list = ["2022-01"]

serial_number = 3245  # Serial 번호 초기화

for folder in folder_list:
    folder_path = os.path.join(directory, folder)
    #file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    file_count = 50
    y_coord = 73  # 초기 y 축 좌표 설정
    y_coord2 = 89  # 두 번째 페이지의 초기 y 축 좌표 설정
    current_file = 0  # 현재 파일 번호 초기화

    print(folder_path + " file count: " + str(file_count))
    
    time.sleep(5)
    
    #data type select    
    pyautogui.click(1700, 270)
    time.sleep(2)   
    #data type-holter select   
    pyautogui.click(1680, 293)
    time.sleep(2) 
    #click patient select 
    pyautogui.click(140, 988)
    time.sleep(2)       

    while current_file < file_count:
        if current_file >= 58:  # 58개 파일을 초과한 후부터 매번 실행
            pyautogui.click(260, 934)  # 스크린 활성화 클릭
            time.sleep(2)
            pyautogui.press('pagedown')
            time.sleep(2)
        if current_file >= 116:  # 116번째 파일부터 pagedown을 추가로 실행
            pyautogui.press('pagedown')
            time.sleep(2)
        if current_file >= 174:  # 174번째 파일부터 pagedown을 추가로 실행
            pyautogui.press('pagedown')
            time.sleep(2)
        if current_file >= 232:  # 174번째 파일부터 pagedown을 추가로 실행
            pyautogui.press('pagedown')
            time.sleep(2)
        if current_file == 116 or current_file == 174 or current_file == 232:  # 116번째 및 207번째 파일에서 y 좌표 초기화
            y_coord2 = 89

        Serial = f"{serial_number}_"

    
        if current_file < 58:
            time.sleep(2)
            pyautogui.click(240, y_coord) 
            time.sleep(2)
            pyautogui.click(240, y_coord) 
            time.sleep(2)
        else:
            time.sleep(2)
            pyautogui.click(240, y_coord2) 
            time.sleep(2)
            pyautogui.click(240, y_coord2) 
            time.sleep(2)

        time.sleep(2)
        pyautogui.click(217, 985)  
        time.sleep(2)
                
        # Serial 뒤에 붙일 값 복사
        pyautogui.click(1200, 90)
        pyautogui.dragTo(1040, 90, duration=1)
        pyautogui.hotkey('ctrl', 'c')
        additional_value = pyperclip.paste()
        Serial += additional_value

        pyautogui.click(26, 36)
        time.sleep(2) 
        #Research Utilities
        pyautogui.click(86, 105)
        time.sleep(2)
        #OK
        pyautogui.click(800, 547)
        time.sleep(2) 
        #change
        pyautogui.click(1100, 473)
        time.sleep(2) 
        pyautogui.write(Serial)
        time.sleep(2)
        pyautogui.click(1580, 620)
        time.sleep(2) 
        #save
        pyautogui.click(1070, 680)
        time.sleep(2)
        #change
        pyautogui.click(1100, 473)
        time.sleep(2) 
        pyautogui.write(Serial)
        time.sleep(2)
        pyautogui.click(1580, 620)
        time.sleep(2) 
        #save
        pyautogui.click(1070, 680)
        time.sleep(5)
        pyautogui.click(1118, 472) 
        time.sleep(2)
        
        #click patient select 
        pyautogui.click(140, 988)
        time.sleep(2)   
            
        # 폴더 처리 전 추가 로직
        pyautogui.click(750, 980)
        time.sleep(5)
        pyautogui.click(1790, 93)
        time.sleep(2)
        pyautogui.click(358, 358)
        time.sleep(2)
        # Serial 값을 붙여넣기
        pyautogui.write(Serial)
        time.sleep(2)
        pyautogui.click(1393, 359)
        time.sleep(2)
        #PDF 저장
        pyautogui.click(1070, 682)
        time.sleep(60)  
        pyautogui.click(140, 985)
        time.sleep(3)
        
        #click patient select 
        pyautogui.click(140, 988)
        time.sleep(2)   

        # Serial 변수 사용 후에 Serial 번호 증가 및 현재 파일 번호 증가
        serial_number += 1
        current_file += 1

        if current_file <= 58:
            y_coord += 15  # 다음 파일의 y 좌표로 업데이트
        else:
            y_coord2 += 15  # 다음 파일의 y 축 좌표 업데이트
        
        print(f"Current file: {current_file}")  # 현재 처리 중인 파일 번호 출력

    # finish
    time.sleep(4)
