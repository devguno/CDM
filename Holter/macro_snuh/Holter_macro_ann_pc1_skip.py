import os
import pyautogui
import pyperclip
import time
import keyboard
from tqdm import tqdm
import math

# Activate fail-safe (program stops if the mouse moves to the top left corner of the screen)
pyautogui.FAILSAFE = False

# Set the specified directory
directory = "C:\\boramae"
folder_list =  ['boramae_201714']
    
# Iterate over all subfolders within the directory
for folder in folder_list:
    folder_path = os.path.join(directory, folder)
    file_count = 200
    y_coord = 73  # Initialize the y-axis coordinate
    y_coord2 = 89  # Initialize the y-axis coordinate for the second page
    current_file = 0  # Initialize the current file number
    iteration_count = 1

    print(folder_path + " file count: " + str(file_count))

    # Wait for the first 5 seconds
    time.sleep(3)
    
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

        Serial = f"{folder}_{iteration_count}_"
    
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
        pyautogui.click(217, 985)  # 특정 작업 수행
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
        #MIT Annotation Format
        pyautogui.click(760, 370)
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
        time.sleep(2)
        #ok
        pyautogui.click(1100, 600)
        time.sleep(2)
        #ok
        pyautogui.click(1070, 600)
        time.sleep(2)
        #ok
        pyautogui.click(1040, 600)
        time.sleep(2)
        #ok
        pyautogui.click(1080, 600)
        time.sleep(2)
        #ok
        pyautogui.click(1100, 600)
        time.sleep(2)
        #ok
        pyautogui.click(1070, 600)
        time.sleep(2)
        #ok
        pyautogui.click(1040, 600)
        time.sleep(2)
        #ok
        pyautogui.click(1080, 600)
        time.sleep(2)
        #OK
        pyautogui.click(1118, 472) 
        time.sleep(2)
        
        #MIT Signal Format
        pyautogui.click(750, 420) 
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
        #overwrite
        pyautogui.click(1000, 540)
        time.sleep(2)
        pyautogui.click(1100, 520)
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
        time.sleep(10)
        #OK
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
        pyautogui.click(400, 410)
        time.sleep(2)
        
        # Serial 값을 붙여넣기
        pyautogui.write(Serial)
        time.sleep(2)
        pyautogui.click(1393, 359)
        time.sleep(2)
        #PDF 저장
        pyautogui.click(1070, 682)
        time.sleep(100)  
        pyautogui.click(140, 985)
        time.sleep(3)
        
        #click patient select 
        pyautogui.click(140, 988)
        time.sleep(2)  
        # If it's the last file, execute the subsequent tasks
        if current_file == file_count:
            time.sleep(3)
            pyautogui.click(400, 72)
            time.sleep(2)
            pyautogui.moveTo(1488, 68)
            pyautogui.dragTo(1488, 922, duration=2.0)
            pyautogui.keyDown('shift')
            pyautogui.click(180, 929)
            pyautogui.keyUp('shift')
            time.sleep(2)
            pyautogui.click(1600, 127)
            time.sleep(2)
            pyautogui.click(1600, 110)
            time.sleep(2)
            pyautogui.click(1100, 550)
            time.sleep(4)
        
        # 3번째 파일마다 특정 동작 실행
        if current_file % 3 == 0 and current_file != 0:  # 첫 번째 파일(인덱스 0)을 제외하고 10의 배수일 때마다 실행
            pyautogui.rightClick(273, 1050)  # MARS program right click, LEFT 5
            time.sleep(2)
            pyautogui.click(273, 1023)  # close window
            time.sleep(4)
            pyautogui.click(273, 1050)  # MARS program click
            time.sleep(4)
            #click patient select 
            pyautogui.click(140, 988)
            time.sleep(2)    

        # Serial 변수 사용 후에 Serial 번호 증가 및 현재 파일 번호 증가
        iteration_count += 1
        current_file += 1

        if current_file <= 58:
            y_coord += 15  # 다음 파일의 y 좌표로 업데이트
        else:
            y_coord2 += 15  # 다음 파일의 y 축 좌표 업데이트
        
        print(f"Current file: {current_file}")  # 현재 처리 중인 파일 번호 출력

    # 이후 작업들
    time.sleep(3)
    #patient select
    pyautogui.click(140, 990)
    time.sleep(2)

