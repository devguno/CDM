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
# Click on the keyboard settings in the bottom menu bars
pyautogui.click(1525, 1025)
time.sleep(2)
# English click
pyautogui.click(1525, 860)
time.sleep(2)
# MARS program click
pyautogui.click(222, 1025) 
time.sleep(2)    
# Activate fail-safe (program stops if the mouse moves to the top left corner of the screen)
pyautogui.FAILSAFE = True

#####
# Set the specified directory
directory = "C:\\Holter"

# # Get all subfolder names within the directory as a list
folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
print(f"folder list: {folder_list}")

#folder_list =  [ '2094', '2095', '2109', '2110', '2111', '2112', '2113', '2106', '2107', '2108']

# Iterate over all subfolders within the directory
for folder in folder_list:
    folder_path = os.path.join(directory, folder)
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    y_coord = 71  
    y_coord2 = 86 
    current_file = 0  
    iteration_count = 1
    
    print(folder_path + " file count: " + str(file_count))
    
    
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
    pyautogui.mouseUp()     # Release the mouse button
    #input folder path
    pyautogui.write(directory + '\\' + folder)
    time.sleep(2)
    #clisk 'save'
    pyautogui.click(1026, 651)  
    time.sleep(2)
    #clisk 'ok'
    pyautogui.click(972, 466)  
    time.sleep(2)
    #click 'Patient Select'
    pyautogui.click(140, 950)  
    time.sleep(2)
    # Click on Data type
    pyautogui.click(1519, 262)  
    time.sleep(2)
    # Click on Data type-Archived files
    pyautogui.click(1519, 319)  
    time.sleep(4)

    # Patient List 에서 첫번째 클릭
    pyautogui.click(350, 70)  
    time.sleep(2) 
    # 스크롤바 가장 위부터 아래까지 드래그(리스트 전체 선택)
    pyautogui.moveTo(1304, 66)  
    pyautogui.dragTo(1304, 895, duration=2.0)  

    # Shift 키를 누른 상태에서 리스트 가장 마지막 클릭
    pyautogui.keyDown('shift')
    pyautogui.click(158, 902)  
    pyautogui.keyUp('shift')
    time.sleep(2)
    
    # 파일당 작업 완료 후 대기 및 다음 작업 수행
    pyautogui.click(1403, 121)  
    time.sleep(2)
    pyautogui.click(1488, 183)  
    time.sleep(2)
    pyautogui.click(962, 544)  
    time.sleep(30)
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
        if current_file >= 116: # 116번째 파일부터 pagedown을 추가로 실행
            pyautogui.press('pagedown')
            time.sleep(2)
        if current_file >= 174:
            pyautogui.press('pagedown')
            time.sleep(2)
        if current_file >= 232:
            pyautogui.press('pagedown')
            time.sleep(2)
        if current_file == 116 or current_file == 174 or current_file == 232:
            y_coord2 = 86

        Serial = f"{folder}_{iteration_count}_"
    
        if current_file < 58:
            time.sleep(2)
            pyautogui.click(210, y_coord)  
            time.sleep(2)
            pyautogui.click(210, y_coord)  
            time.sleep(2)
        else:
            time.sleep(2)
            pyautogui.click(210, y_coord2)  
            time.sleep(2)
            pyautogui.click(210, y_coord2)  
            time.sleep(2)

        time.sleep(2)
        
        #clock 'Patient Information'
        pyautogui.click(215, 955)  
        time.sleep(2)
                
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
        time.sleep(5)
        pyautogui.click(979, 459)  
        time.sleep(2)
        
        #click patient select 
        pyautogui.click(140, 950) 
        time.sleep(2)  
        #click "Report Review"
        pyautogui.click(750, 955)  
        time.sleep(4)
        #click print report
        pyautogui.click(1596, 90) 
        time.sleep(2)
        pyautogui.click(313, 348)  
        time.sleep(2)
        
        # Serial 값을 붙여넣기
        pyautogui.write(Serial)
        time.sleep(2)
        pyautogui.click(1219, 348) 
        time.sleep(2)
        #PDF 저장
        pyautogui.click(937, 661)  
        time.sleep(50)  
        pyautogui.click(122, 1021) 
        time.sleep(3)
        
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
            
        # 3번째 파일마다 MARS program re-start
        if current_file % 3 == 0 and current_file != 0: 
            pyautogui.rightClick(222, 1020)  
            time.sleep(2)
            pyautogui.click(222, 1000) 
            time.sleep(4)
            pyautogui.click(222, 1020)  
            time.sleep(4)
            #click patient select 
            pyautogui.click(140, 950) 
            time.sleep(2)

        current_file += 1

        if current_file <= 58:
            y_coord += 14  
        else:
            y_coord2 += 14 
        
        print(f"Current file: {current_file}") 

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
    pyautogui.click(1403, 111) 
    time.sleep(2)
    pyautogui.click(1575, 96)  
    time.sleep(2)
    pyautogui.click(962, 529)  
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
    pyautogui.click(1403, 111) 
    time.sleep(2)
    pyautogui.click(1575, 96)  
    time.sleep(2)
    pyautogui.click(962, 529)  
    time.sleep(2)
    #click patient select 
    pyautogui.click(140, 950) 
    time.sleep(2)