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

folder_list = ["2011-08", "2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06"]

serial_number = 1  # Serial 번호 초기화

for folder in folder_list:
    folder_path = os.path.join(directory, folder)
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])

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
    pyautogui.mouseDown()        # 마우스 버튼을 누른 상태로 유지
    pyautogui.moveTo(1232, 387, duration=1)  # 드래그 위치로 이동
    pyautogui.mouseUp()          # 마우스 버튼을 놓아 드래그 완료
    
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
    time.sleep(400)
    pyautogui.click(1107, 475)
    time.sleep(1)
    pyautogui.click(1700, 310)
    time.sleep(1)    
    pyautogui.click(1700, 270)
    time.sleep(1)    
    pyautogui.click(1680, 293)
    time.sleep(1)       
    # 폴더 내의 파일 수만큼 반복
    folder_path = os.path.join(directory, folder)
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    
    y_coord = 73  # 초기 y 축 좌표 설정
    current_file = 0  # 현재 파일 번호 초기화

    while current_file < file_count - 1:
        for _ in tqdm(range(min(62, file_count - current_file)), desc=f"Processing files in {folder}"):
            # Serial 번호와 함께 Serial 변수 생성
            Serial = f"{serial_number}_"
            
            pyautogui.click(240, y_coord)
            time.sleep(1)
            pyautogui.click(217, 985)
            time.sleep(1)
                
            # Serial 뒤에 붙일 값 복사
            pyautogui.click(1200, 90)
            pyautogui.dragTo(1040, 90, duration=1)
            pyautogui.hotkey('ctrl', 'c')
            additional_value = pyperclip.paste()
            Serial += additional_value

            pyautogui.click(26, 36)
            time.sleep(1) 
            #Research Utilities
            pyautogui.click(86, 105)
            time.sleep(1)
            #OK
            pyautogui.click(800, 547)
            time.sleep(1) 
            #change
            pyautogui.click(1100, 473)
            time.sleep(1) 
            pyautogui.write(Serial)
            time.sleep(1)
            pyautogui.click(1580, 620)
            time.sleep(1) 
            #save
            pyautogui.click(1070, 680)
            time.sleep(1)
            #change
            pyautogui.click(1100, 473)
            time.sleep(1) 
            pyautogui.write(Serial)
            time.sleep(1)
            pyautogui.click(1580, 620)
            time.sleep(1) 
            #save
            pyautogui.click(1070, 680)
            time.sleep(5)
            pyautogui.click(1118, 472) 
            time.sleep(1)
            pyautogui.click(143, 987) 
            time.sleep(1)
            
            # 폴더 처리 전 추가 로직
            pyautogui.click(750, 980)
            time.sleep(1)
            pyautogui.click(1790, 93)
            time.sleep(1)
            pyautogui.click(358, 358)
            time.sleep(1)
            
            # Serial 값을 붙여넣기
            pyautogui.write(Serial)
            time.sleep(1)
            pyautogui.click(1393, 359)
            time.sleep(1)
            #PDF 저장
            pyautogui.click(1070, 682)
            time.sleep(50)  
            pyautogui.click(140, 985)
            time.sleep(1)

            # Serial 변수 사용 후에 Serial 번호 증가 및 현재 파일 번호 증가
            serial_number += 1
            current_file += 1

            # y 축 좌표 업데이트
            y_coord += 14
            print(current_file)
            
        if current_file < file_count - 1:  # 마지막 페이지가 아니라면 PageDown
            time.sleep(1)  
            pyautogui.click(140, 985)
            time.sleep(1)
            pyautogui.click(240, 930)
            time.sleep(1)
            pyautogui.press('pagedown')
            time.sleep(1)  # 페이지 다운 후 잠시 대기
            y_coord = 87  # y 축 좌표 초기화
            
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

    # 추가 클릭 작업
    pyautogui.click(1600, 127)
    time.sleep(1)
    pyautogui.click(1600, 110)
    time.sleep(1)
    pyautogui.click(1100, 550)
    time.sleep(2)

    # 반복 사이에 짧은 지연 시간
    time.sleep(3)