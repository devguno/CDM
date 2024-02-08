import os
import pyautogui
import pyperclip
import time
import keyboard
from tqdm import tqdm
import math

# 지정된 디렉토리 설정
directory = "Z:\\Holter\\Holter_child_hdd"

# # 디렉토리 내의 모든 하위 폴더명을 리스트로 가져오기
# folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

folder_list = ["2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06"]

serial_number = 1  # Serial 번호 초기화

for folder in folder_list:
    folder_path = os.path.join(directory, folder)
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    
    y_coord = 73  # 초기 y 축 좌표 설정
    y_coord2 = 89  # 초기 y 축 좌표 설정
    current_file = 0  # 현재 파일 번호 초기화
    
    print(folder_path + " file count: " + str(file_count))
    
    time.sleep(5)
    
    # 1. 26,36 pixels 의 좌표를 왼쪽 클릭
    pyautogui.click(26, 36)
    time.sleep(1)
    # 2. 72,78 pixels 의 좌표로 마우스 이동
    pyautogui.moveTo(72, 78)
    time.sleep(1)
    # 3. 264,373 pixels 의 좌표를 왼쪽 클릭
    pyautogui.click(264, 373)
    time.sleep(1)
    # 4. 1394,387 pixels의 좌표를 클릭하고 1232,387 pixels 의 좌표까지 드래그
    pyautogui.moveTo(1394, 387)  # 시작 위치로 이동
    pyautogui.mouseDown()        
    pyautogui.moveTo(1232, 387, duration=1)  # 드래그 위치로 이동
    pyautogui.mouseUp()          
    
    # 5. folder_list에 있는 첫번째 값을 붙여 넣기
    pyautogui.write(folder)
    pyautogui.press('enter') # 필요에 따라 Enter 키를 누를 수 있습니다.
    time.sleep(1)
    # 6. 1172,670 pixels 의 좌표를 왼쪽 클릭
    pyautogui.click(1172, 670)
    time.sleep(1)
    # 7. 1110,480 pixels 의 좌표를 왼쪽 클릭
    pyautogui.click(1110, 480)
    time.sleep(1)
    # 8. 140,980 pixels 의 좌표를 왼쪽 클릭
    pyautogui.click(140, 980)
    time.sleep(1)
    # Data type
    pyautogui.click(1735, 270)
    time.sleep(1)
    pyautogui.click(1735, 328)
    time.sleep(1)
    pyautogui.click(400, 72)
    time.sleep(1)
    
    # Fail-safe 활성화
    pyautogui.FAILSAFE = True

    # (400, 72) 위치를 클릭
    pyautogui.click(400, 72)
    time.sleep(1)  # 1초 대기

    # (1488, 68)에서 (1488, 922)까지 드래그
    pyautogui.moveTo(1488, 68)
    pyautogui.dragTo(1488, 922, duration=1.0)  # 드래그하는 동안 1초간 지속

    # Shift 키를 누른 상태에서 (180, 929) 위치를 클릭
    pyautogui.keyDown('shift')  # Shift 키를 누름
    pyautogui.click(180, 929)   # 클릭
    pyautogui.keyUp('shift')    # Shift 키를 놓음
    
    
    # 파일당 작업 완료 후 대기 및 다음 작업 수행
    pyautogui.click(1604, 124)
    time.sleep(1)
    pyautogui.click(1700, 188)
    time.sleep(1)
    pyautogui.click(1100, 560)
    #Archive 대기 시간
    time.sleep(700)
    pyautogui.click(1107, 475)
    time.sleep(1)
    #click close
    pyautogui.click(1700, 310)
    time.sleep(1)
    #data type select    
    pyautogui.click(1700, 270)
    time.sleep(1)   
    #data type-holter select   
    pyautogui.click(1680, 293)
    time.sleep(1) 
    #click patient select 
    pyautogui.click(140, 988)
    time.sleep(2)       

    while current_file < file_count:
        if current_file >= 60:  # 62개 파일을 초과한 후부터 매번 실행
            pyautogui.click(260, 934)  # 스크린 활성화 클릭
            time.sleep(1)
            pyautogui.press('pagedown')
            time.sleep(1)
        if current_file >= 120:  # 145번째 파일부터 pagedown을 추가로 실행
            pyautogui.press('pagedown')
            time.sleep(1)
        if current_file >= 180:  # 206번째 파일부터 pagedown을 추가로 실행
            pyautogui.press('pagedown')
            time.sleep(1)
        if current_file == 120 or current_file == 180:  # 145번째 및 207번째 파일에서 y 좌표 초기화
            y_coord2 = 89

        Serial = f"{serial_number}_"

        if current_file < 60:
            pyautogui.click(240, y_coord)  # 처음 62개 파일 처리
        else:
            pyautogui.click(240, y_coord2)  # 62개 이후 파일 처리

        time.sleep(1)
        pyautogui.click(217, 985)  # 특정 작업 수행
        time.sleep(1)
        pyautogui.click(140, 985)  # 다른 작업 수행
        time.sleep(1)

        serial_number += 1
        current_file += 1

        if current_file <= 60:
            y_coord += 15  # 다음 파일의 y 좌표로 업데이트
        else:
            y_coord2 += 15  # 다음 파일의 y 축 좌표 업데이트
        
        print(f"Current file: {current_file}")  # 현재 처리 중인 파일 번호 출력

    # 이후 작업들
    pyautogui.click(400, 72)
    time.sleep(1)
    pyautogui.moveTo(1488, 68)
    pyautogui.dragTo(1488, 922, duration=1.0)
    pyautogui.keyDown('shift')
    pyautogui.click(180, 929)
    pyautogui.keyUp('shift')

    pyautogui.click(1600, 127)
    time.sleep(1)
    pyautogui.click(1600, 110)
    time.sleep(1)
    pyautogui.click(1100, 550)
    time.sleep(2)

    time.sleep(3)