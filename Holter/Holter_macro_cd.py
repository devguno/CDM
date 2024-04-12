import os
import pyautogui
import pyperclip
import time
import keyboard
from tqdm import tqdm
import math

### Note: The MARS program should be set to use the keyboard in English. Make sure to set the keyboard layout to English before starting.
# Wait for 2 seconds after starting the code
time.sleep(2)
# Click on the keyboard settings in the bottom menu bar
pyautogui.click(1780, 1035)
time.sleep(2)
# Click on Menu-System-System setup
pyautogui.moveTo(1780, 830)
time.sleep(2)
    
# Activate fail-safe (program stops if the mouse moves to the top left corner of the screen)
pyautogui.FAILSAFE = True

#####
# Set the specified directory
directory = "Z:\Holter\Holter_gangnam"

# # Get all subfolder names within the directory as a list
folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
print(f"folder list: {folder_list}")

serial_number = 5000 # Initialize the serial number

# Iterate over all subfolders within the directory
for folder in folder_list:
    folder_path = os.path.join(directory, folder)
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    y_coord = 73  # Initialize the y-axis coordinate
    y_coord2 = 89  # Initialize the y-axis coordinate for the second page
    current_file = 0  # Initialize the current file number

    print(folder_path + " file count: " + str(file_count))

    # Wait for the first 5 seconds
    time.sleep(5)
    # Click on Menu-System
    pyautogui.click(26, 36)
    time.sleep(2)
    # Click on Menu-System-System setup
    pyautogui.moveTo(72, 78)
    time.sleep(2)
    # Click on Menu-System-System setup-General
    pyautogui.click(264, 373)
    time.sleep(2)
    # Update Archive Path name by dragging and pasting
    pyautogui.moveTo(1440, 400)  # Move to the starting position
    pyautogui.mouseDown()        # Press and hold the mouse button
    pyautogui.moveTo(1000, 400, duration=2)  # Move to the drag position
    pyautogui.mouseUp()          # Release the mouse button

    # Paste the value from folder_list
    pyautogui.write(directory + '\\' + folder)
    time.sleep(2)
    # Click on save
    pyautogui.click(1172, 670)
    time.sleep(2)
    # Click on ok
    pyautogui.click(1110, 480)
    time.sleep(2)
    # Click on Patient Select at the bottom
    pyautogui.click(140, 980)
    time.sleep(2)
    # Click on Data type
    pyautogui.click(1735, 270)
    time.sleep(2)
    # Click on Data type-Archived files
    pyautogui.click(1735, 328)
    time.sleep(2)

    # Patient List 에서 첫번째 클릭
    pyautogui.click(400, 72)
    time.sleep(2) 
    # 스크롤바 가장 위부터 아래까지 드래그(리스트 전체 선택)
    pyautogui.moveTo(1488, 68)
    pyautogui.dragTo(1488, 922, duration=2.0)  # 드래그 2초간 지속

    # Shift 키를 누른 상태에서 리스트 가장 마지막 클릭
    pyautogui.keyDown('shift')  # Shift 키를 누름
    pyautogui.click(180, 929)  
    pyautogui.keyUp('shift')    # Shift 키를 놓음
    time.sleep(2)
    
    # 파일당 작업 완료 후 대기 및 다음 작업 수행
    pyautogui.click(1604, 124)
    time.sleep(2)
    pyautogui.click(1700, 188)
    time.sleep(2)
    pyautogui.click(1100, 560)
    #Archive 대기 시간
    time.sleep(400)
    pyautogui.click(860,1045)
    #Archive 대기 시간
    time.sleep(400)
    pyautogui.click(860,1045)
    #Archive 대기 시간
    time.sleep(400)
    pyautogui.click(860,1045)
    #Archive 대기 시간
    time.sleep(400)
    pyautogui.click(1107, 475)
    time.sleep(2)
    #click close
    pyautogui.click(1700, 310)
    time.sleep(2)
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
        time.sleep(30)
        #time.sleep(200)
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
        time.sleep(100)  
        pyautogui.click(140, 985)
        time.sleep(3)
        
        #click patient select 
        pyautogui.click(140, 988)
        time.sleep(2)  
        
        # 10번째 파일마다 특정 동작 실행
        if current_file % 2 == 0 and current_file != 0:  # 첫 번째 파일(인덱스 0)을 제외하고 10의 배수일 때마다 실행
            pyautogui.click(1900, 17)  # 지정된 좌표 클릭
            time.sleep(5)
            pyautogui.click(325, 1045)  # 지정된 좌표 클릭
            time.sleep(5)
            pyautogui.click(140, 988)  # 지정된 좌표 클릭
            time.sleep(5)

        # Serial 변수 사용 후에 Serial 번호 증가 및 현재 파일 번호 증가
        serial_number += 1
        current_file += 1

        if current_file <= 58:
            y_coord += 15  # 다음 파일의 y 좌표로 업데이트
        else:
            y_coord2 += 15  # 다음 파일의 y 축 좌표 업데이트
        
        print(f"Current file: {current_file}")  # 현재 처리 중인 파일 번호 출력

    # 이후 작업들
    time.sleep(3)
    pyautogui.click(400, 72)
    time.sleep(2)
    pyautogui.moveTo(1488, 68)
    pyautogui.dragTo(1488, 922, duration=1.0)
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
