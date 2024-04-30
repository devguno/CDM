import os
import pyautogui
import pyperclip
import time
import keyboard
from tqdm import tqdm
import math

### Note: The MARS program should be set to use the keyboard in English. Make sure to set the keyboard layout to English before starting.
# Wait for 4 seconds after starting the code
time.sleep(4)
# Click on the keyboard settings in the bottom menu bars
pyautogui.click(1780, 1050)
time.sleep(2)
# English click
pyautogui.click(1780, 827)
time.sleep(2)
# MARS program click
pyautogui.click(273, 1050) 
time.sleep(5)
    
# Activate fail-safe (program stops if the mouse moves to the top left corner of the screen)
pyautogui.FAILSAFE = True

#####
# Set the specified directory
directory = "Z:\Holter_cdrom"

# # Get all subfolder names within the directory as a list
#folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
#print(f"folder list: {folder_list}")
#'DVD20081111', 'DVD20081128', 'DVD20081229', 'DVD20090122','DVD20090309', 'DVD20090405', 'DVD20090511', 'DVD20090615', 'DVD20090714', 'DVD20090806', 
#'DVD20090902', 'DVD20090930', 'DVD20091103', 'DVD20091204', 'DVD20091230','DVD20100118', 'DVD20100204', 'DVD20100225', 'DVD20100322','DVD20100414', 
#'DVD20100513', 'DVD20100616', 'DVD20100710', 'DVD20100730', 'DVD20100820','DVD20100916', 'DVD20101009', 'DVD20101026', 'DVD20101229', 'DVD20110119', 
#'DVD20110208', 'DVD20110224', 'DVD20110417', 'DVD20110502', 'DVD20110523', 'DVD20110614', 'DVD20110701', 'DVD20110721', 'DVD20110804', 'DVD20110817', 
#'DVD20110831', 'DVD20110928', 'DVD20111019', 'DVD20111114', 'DVD20111210', 'DVD20120103', 'DVD20120111', 'DVD20120118', 'DVD20120202', 'DVD20120216', 
#'DVD20120227', 'DVD20120320', 'DVD20120413', 'DVD20120509', 'DVD20120602', 'DVD20120627', 'DVD20120629', 'DVD20120723', 'DVD20120807', 'DVD20120827', 
folder_list = ['DVD20120924', 'DVD20121017', 'DVD20121112', 'DVD20121128', 'DVD20121213', 'DVD20130102', 'DVD20130115', 'DVD20130129', 'DVD20130214', 'DVD20130227', 
               'DVD20130321', 'DVD20130408', 'DVD20130429', 'DVD20130523', 'DVD20130611', 'DVD20130628', 'DVD20130723', 'DVD20130808', 'DVD20130826', 'DVD20130923', 
               'DVD20131024', 'DVD20131118', 'DVD20131211', 'DVD20131231', 'DVD20140116', 'DVD20140206', 'DVD20140225', 'DVD20140315', 'DVD20140410', 'DVD20140509', 
               'DVD20140610', 'DVD20140715', 'DVD20140801', 'DVD20140827', 'DVD20140911', 'DVD20141106', 'DVD20141211', 'DVD20141224', 'DVD20150120', 'DVD20150203', 
               'DVD20150224', 'DVD20150308', 'DVD20150403', 'DVD20150424', 'DVD20150522', 'DVD20150629', 'DVD20150724', 'DVD20150812', 'DVD20150917', 'DVD20151016', 
               'DVD20151112', 'DVD20151215', 'DVD20160107', 'DVD20160121', 'DVD20160211', 'DVD20160225', 'DVD20160325', 'DVD20160518', 'DVD20160615', 'DVD20160712', 
               'DVD20160802', 'DVD20160819', 'DVD20160909', 'DVD20161017', 'DVD20161116', 'DVD20161214', 'DVD20170103', 'DVD20170124', 'DVD20170215', 'DVD20170309', 
               'DVD20170406', 'DVD20170504', 'DVD20170531', 'DVD20170621', 'DVD20170718', 'DVD20170808', 'DVD20170830', 'DVD20171010', 'DVD20171113', 'DVD20171208', 
               'DVD20180102', 'DVD20180123', 'DVD20180219', 'DVD20180307', 'DVD20180403', 'DVD20180502', 'DVD20180531', 'DVD20180628', 'DVD20180719', 'DVD20180807', 
               'DVD20180827', 'DVD20180928', 'DVD20181106', 'DVD20181129', 'DVD20181221', 'DVD20190115', 'DVD20190130', 'DVD20190219', 'DVD20190308', 'DVD20190402', 
               'DVD20190426', 'DVD20190526', 'DVD20190618', 'DVD20190711', 'DVD20190802', 'DVD20190820', 'DVD20190910', 'DVD20191014', 'DVD20191112', 'DVD20191204']

serial_number = 14600 # Initialize the serial number

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
    time.sleep(2)
    #Archive 대기 시간
    time.sleep(400)
    pyautogui.click(860,1045)
    #Archive 대기 시간
    time.sleep(400)
    pyautogui.click(860,1045)
    #Archive 대기 시간
    #click close
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
        time.sleep(10)
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
        
        # 2번째 파일마다 특정 동작 실행
        if current_file % 2 == 0 and current_file != 0:  # 첫 번째 파일(인덱스 0)을 제외하고 10의 배수일 때마다 실행
            pyautogui.rightClick(273, 1050)  # MARS program right click
            time.sleep(2)
            pyautogui.click(273, 1023)  # close window
            time.sleep(4)
            pyautogui.click(273, 1050)  # MARS program click
            time.sleep(4)
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

    # 이후 작업들
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
