import os
import pyautogui
import pyperclip
import time
import keyboard
from tqdm import tqdm
import math

### Note: The MARS program should be set to use the keyboard in English. Make sure to set the keyboard layout to English before starting.
time.sleep(3)
# Click on the keyboard settings in the bottom menu bars
pyautogui.click(1525, 1025)
time.sleep(2)
# English click
pyautogui.click(1525, 860)
time.sleep(2)
# MARS program click
pyautogui.click(222, 1025) 
time.sleep(5)
    
# Activate fail-safe (program stops if the mouse moves to the top left corner of the screen)d
pyautogui.FAILSAFE = True

#####
# Set the specified directory
directory = "C:\\holter"
# # Get all subfolder names within the directory as a list
#folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
#print(f"folder list: {folder_list}")
folder_list =  ['2336','2337','2338','2339','2340','2341','2342','2343','2344','2345','2346','2347','2348','2349']
    
# Iterate over all subfolders within the directory
for folder in folder_list:
    folder_path = os.path.join(directory, folder)
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])-1
    y_coord = 71  # Initialize the y-axis coordinate
    y_coord2 = 86  # Initialize the y-axis coordinate for the second page
    current_file = 0  # Initialize the current file number
    iteration_count = 1

    print(folder_path + " file count: " + str(file_count))

    # Wait for the first 5 seconds
    time.sleep(5)
    # Click on Menu-System
    pyautogui.click(23, 35)  
    time.sleep(2)
    # Click on Menu-System-System setup
    pyautogui.moveTo(63, 76)  
    time.sleep(2)
    # Click on Menu-System-System setup-General
    pyautogui.click(231, 362)  
    time.sleep(2)
    # Update Archive Path name by dragging and pasting
    pyautogui.moveTo(1260, 388)  # Move to the starting position
    pyautogui.mouseDown()        # Press and hold the mouse button
    pyautogui.moveTo(875, 388, duration=2)  # Move to the drag position
    pyautogui.mouseUp()          # Release the mouse button

    # Paste the value from folder_list
    pyautogui.write(directory + '\\' + folder)
    time.sleep(2)
    # Click on save
    pyautogui.click(1026, 651)  
    time.sleep(2)
    # Click on ok
    pyautogui.click(972, 466)  
    time.sleep(2)
    # Click on Patient Select at the bottom
    pyautogui.click(140, 950)  
    time.sleep(2)
    # Click on Data type
    pyautogui.click(1519, 262)  
    time.sleep(2)
    # Click on Data type-Archived files
    pyautogui.click(1519, 319)  
    time.sleep(6)

    # Patient List 에서 첫번째 클릭
    pyautogui.click(350, 70)  
    time.sleep(2) 
    # 스크롤바 가장 위부터 아래까지 드래그(리스트 전체 선택)
    pyautogui.moveTo(1304, 66)  
    pyautogui.dragTo(1304, 895, duration=2.0)  

    # Shift 키를 누른 상태에서 리스트 가장 마지막 클릭
    pyautogui.keyDown('shift')  # Shift 키를 누름
    pyautogui.click(158, 902)  
    pyautogui.keyUp('shift')    # Shift 키를 놓음
    time.sleep(2)
    
    # 파일당 작업 완료 후 대기 및 다음 작업 수행
    pyautogui.click(1403, 121)  
    time.sleep(2)
    pyautogui.click(1488, 183)  
    time.sleep(2)
    pyautogui.click(962, 544)  
    time.sleep(5)
    pyautogui.click(962, 554)  
    time.sleep(10)
    #click close
    pyautogui.click(970, 461)  
    time.sleep(2)
    #click patient select 
    pyautogui.click(140, 950)   
    time.sleep(2)  

    while current_file < file_count:
        if current_file >= 58:  # 58개 파일을 초과한 후부터 매번 실행
            pyautogui.click(228, 907)   # 스크린 활성화 클릭
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
        pyautogui.click(215, 955)  
        time.sleep(2)
                
        # Serial 뒤에 붙일 값 복사
        pyautogui.click(1050, 87)  
        pyautogui.dragTo(910, 87, duration=1) 
        pyautogui.hotkey('ctrl', 'c')
        additional_value = pyperclip.paste()
        Serial += additional_value

        pyautogui.click(23, 35)  
        time.sleep(2) 
        #Research Utilities
        pyautogui.click(75, 102)  
        time.sleep(2)
        #OK
        pyautogui.click(700, 531)  
        time.sleep(2) 
        #change
        pyautogui.click(962, 459)  
        time.sleep(2) 
        pyautogui.write(Serial)
        time.sleep(2)
        pyautogui.click(1382, 602)  
        time.sleep(2) 
        #save
        pyautogui.click(1080, 675)  
        time.sleep(2)
        #change
        pyautogui.click(962, 459)  
        time.sleep(2) 
        pyautogui.write(Serial)
        time.sleep(2)
        pyautogui.click(1382, 602)  
        time.sleep(2) 
        #save
        pyautogui.click(1080, 675)  
        time.sleep(10)
        pyautogui.click(979, 459)  
        time.sleep(2)
        
        #click patient select 
        pyautogui.click(140, 950) 
        time.sleep(2)  
        
        # 폴더 처리 전 추가 로직
        pyautogui.click(750, 955)  
        time.sleep(5)
        pyautogui.click(1596, 90) 
        time.sleep(2)
        pyautogui.click(390, 415)  
        time.sleep(2)
        
        # Serial 값을 붙여넣기
        pyautogui.write(Serial)
        time.sleep(2)
        pyautogui.click(1219, 900) 
        time.sleep(2)
        #PDF 저장
        pyautogui.click(1090, 680)  
        time.sleep(60)  
        
        #click patient select 
        pyautogui.click(140, 950) 
        time.sleep(2)  
        # If it's the last file, execute the subsequent tasks
        if current_file == file_count:
            time.sleep(3)
            pyautogui.click(350, 70)  
            time.sleep(2)
            pyautogui.moveTo(1304, 66) 
            pyautogui.dragTo(1304, 895, duration=2.0)  
            pyautogui.keyDown('shift')
            pyautogui.click(158, 902) 
            pyautogui.keyUp('shift')
            time.sleep(2)
            pyautogui.click(1403, 111) 
            time.sleep(2)
            pyautogui.click(1403, 96)  
            time.sleep(2)
            pyautogui.click(962, 533)  
            time.sleep(4)
        
        # 4번째 파일마다 특정 동작 실행
        if current_file % 4 == 0 and current_file != 0:  # 첫 번째 파일(인덱스 0)을 제외하고 10의 배수일 때마다 실행
            pyautogui.rightClick(222, 1020)  
            time.sleep(2)
            pyautogui.click(222, 1000) 
            time.sleep(4)
            pyautogui.click(222, 1020)  
            time.sleep(4)
            #click patient select 
            pyautogui.click(140, 950) 
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
    pyautogui.click(350, 70) 
    time.sleep(2)
    pyautogui.moveTo(1304, 66)
    pyautogui.dragTo(1304, 895, duration=2.0)  
    pyautogui.keyDown('shift')
    pyautogui.click(158, 902)  
    pyautogui.keyUp('shift')
    time.sleep(2)
    #Tools
    pyautogui.click(1403, 111) 
    time.sleep(2)
    #unlock
    pyautogui.click(1575, 96)  
    time.sleep(2)
    #click patient select 
    pyautogui.click(140, 950) 
    time.sleep(2)
    #first patient click
    pyautogui.click(350, 70)  
    time.sleep(2)
    pyautogui.moveTo(1304, 66)  
    pyautogui.dragTo(1304, 895, duration=2.0) 
    pyautogui.keyDown('shift')
    pyautogui.click(158, 902)  
    pyautogui.keyUp('shift')
    time.sleep(2)
    #Tools
    pyautogui.click(1403, 111) 
    time.sleep(2)
    #delete
    pyautogui.click(1403, 111) 
    time.sleep(2)
    #delete to all 
    pyautogui.click(1000, 530) 
    time.sleep(4)
    #click patient select 
    pyautogui.click(140, 950) 
    time.sleep(2)
    # 한번더 반복
    pyautogui.click(350, 70) 
    time.sleep(2)
    pyautogui.moveTo(1304, 66)
    pyautogui.dragTo(1304, 895, duration=2.0)  
    pyautogui.keyDown('shift')
    pyautogui.click(158, 902)  
    pyautogui.keyUp('shift')
    time.sleep(2)
    #Tools
    pyautogui.click(1403, 111) 
    time.sleep(2)
    #unlock
    pyautogui.click(1575, 96)  
    time.sleep(2)
    #click patient select 
    pyautogui.click(140, 950) 
    time.sleep(2)
    pyautogui.click(350, 70) 
    time.sleep(2)
    pyautogui.moveTo(1304, 66)  
    pyautogui.dragTo(1304, 895, duration=2.0)  
    pyautogui.keyDown('shift')
    pyautogui.click(158, 902)  
    pyautogui.keyUp('shift')
    time.sleep(2)
    #Tools
    pyautogui.click(1403, 111) 
    time.sleep(2)
    #delete
    pyautogui.click(1403, 111) 
    time.sleep(2)
    #delete to all 
    pyautogui.click(1000, 530) 
    time.sleep(4)
    #click patient select 
    pyautogui.click(140, 950) 
    time.sleep(2)
    # 한번더 반복
    pyautogui.click(350, 70) 
    time.sleep(2)
    pyautogui.moveTo(1304, 66)
    pyautogui.dragTo(1304, 895, duration=2.0)  
    pyautogui.keyDown('shift')
    pyautogui.click(158, 902)  
    pyautogui.keyUp('shift')
    time.sleep(2)
    #Tools
    pyautogui.click(1403, 111) 
    time.sleep(2)
    #unlock
    pyautogui.click(1575, 96)  
    time.sleep(2)
    #click patient select 
    pyautogui.click(140, 950) 
    time.sleep(2)
    pyautogui.click(350, 70) 
    time.sleep(2)
    pyautogui.moveTo(1304, 66)  
    pyautogui.dragTo(1304, 895, duration=2.0)  
    pyautogui.keyDown('shift')
    pyautogui.click(158, 902)  
    pyautogui.keyUp('shift')
    time.sleep(2)
    #Tools
    pyautogui.click(1403, 111) 
    time.sleep(2)
    #delete
    pyautogui.click(1403, 111) 
    time.sleep(2)
    #delete to all 
    pyautogui.click(1000, 530) 
    time.sleep(4)
    #click patient select 
    pyautogui.click(140, 950) 
    time.sleep(2)