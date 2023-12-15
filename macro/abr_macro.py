import tkinter as tk
import threading
import pyautogui
import time
import keyboard

data_counter = 1  # 전역 변수로 데이터 카운터를 정의

def macro_1():
    global data_counter  # 전역 변수 사용 선언
    y_offset = 0
    for i in range(35):
        pyautogui.doubleClick(100, 160 + y_offset)
        time.sleep(1)
        pyautogui.doubleClick(100, 175 + y_offset)
        time.sleep(1)
        
        # 여러 위치 클릭
        pyautogui.click(22, 40)
        time.sleep(1)
        pyautogui.click(82, 158)
        time.sleep(1)
        pyautogui.click(261, 181)
        time.sleep(1)
        pyautogui.click(970, 580)
        time.sleep(1)
        pyautogui.click(1060, 875)
        time.sleep(1)

        # 데이터 입력
        pyautogui.write('data{}'.format(data_counter), interval=0.25)
        data_counter += 1
        time.sleep(1)

        # 마지막 위치 클릭
        pyautogui.click(1610, 940)
        time.sleep(1)

        # 첫 번째 위치로 돌아가서 더블 클릭
        pyautogui.doubleClick(100, 160 + y_offset)
        time.sleep(1)

        y_offset += 18

def macro_2():
    global data_counter  # 전역 변수 사용 선언
    y_offset = 0
    for i in range(35):
        pyautogui.doubleClick(100, 180 + y_offset)
        time.sleep(1)
        pyautogui.doubleClick(100, 200 + y_offset)
        time.sleep(1)
        
        # 여러 위치 클릭
        pyautogui.click(22, 40)
        time.sleep(1)
        pyautogui.click(82, 158)
        time.sleep(1)
        pyautogui.click(261, 181)
        time.sleep(1)
        pyautogui.click(970, 580)
        time.sleep(1)
        pyautogui.click(1060, 875)
        time.sleep(1)

        # 데이터 입력
        pyautogui.write('data{}'.format(data_counter), interval=0.25)
        data_counter += 1
        time.sleep(1)

        # 마지막 위치 클릭
        pyautogui.click(1610, 940)
        time.sleep(1)

        # 첫 번째 위치로 돌아가서 더블 클릭
        pyautogui.doubleClick(100, 180 + y_offset)
        time.sleep(1)

        y_offset += 18

def start_macro_thread():
    max_pages = 300
    macro_1()  # macro_1은 한 번만 실행
    for _ in range(max_pages - 1):  # macro_2는 나머지 페이지에서 실행
        keyboard.press_and_release('pagedown')
        time.sleep(2)
        macro_2()

# Tkinter GUI 생성
root = tk.Tk()
root.title("Python Macro")
root.geometry("300x100")
start_button = tk.Button(root, text="Start Macro", command=start_macro_thread)
start_button.pack(pady=20)

root.mainloop()