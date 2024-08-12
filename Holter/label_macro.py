import pyautogui
import time
import pyperclip
import pytesseract
from PIL import ImageGrab
import re

# 클립보드에서 텍스트 가져와 나이로 반환
def get_age_from_clipboard():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    text = pyperclip.paste()
    try:
        return int(text.strip())
    except ValueError:
        return None

# 이미지에서 텍스트 추출 및 숫자 반환
def extract_number_from_image(x1, y1, x2, y2):
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    text = pytesseract.image_to_string(screenshot)
    numbers = re.findall(r'\d+', text)
    return int(numbers[0]) if numbers else None

# 기본 클릭 동작 함수
def perform_basic_clicks():
    pyautogui.click(368, 950)
    time.sleep(2)
    pyautogui.click(1484, 88)
    time.sleep(2)
    pyautogui.click(1395, 167)
    time.sleep(2)
    pyautogui.click(1480, 77)
    time.sleep(2)

# Sinus Heart Rate 설정 함수
def set_sinus_heart_rate(lower, upper):
    pyautogui.click(1580, 100)
    pyautogui.dragTo(1540, 100, duration=1)
    pyautogui.typewrite(str(lower))
    time.sleep(2)
    pyautogui.click(1580, 135)
    time.sleep(2)
    pyautogui.click(1580, 135)
    pyautogui.dragTo(1540, 135, duration=1)
    pyautogui.typewrite(str(upper))
    time.sleep(2)
    pyautogui.click(1500, 340)
    time.sleep(2)
    pyautogui.click(1580, 535)
    time.sleep(2)
    pyautogui.click(1480, 575)
    time.sleep(2)

# 초기 클릭 작업
def initial_clicks():
    pyautogui.click(140, 950)
    time.sleep(2)
    pyautogui.click(350, 70)
    time.sleep(2)
    pyautogui.click(218, 950)
    time.sleep(2)
    pyautogui.moveTo(640, 125)
    pyautogui.dragTo(570, 125, duration=1)
    time.sleep(2)

# 메인 작업 수행
def main_workflow():
    initial_clicks()
    age = get_age_from_clipboard()

    if age == 0:
        perform_basic_clicks()
        set_sinus_heart_rate(100, 180)
    elif 1 <= age <= 5:
        perform_basic_clicks()
        set_sinus_heart_rate(70, 160)
    elif 6 <= age <= 10:
        perform_basic_clicks()
        set_sinus_heart_rate(65, 140)

    pyautogui.click(1460, 507)
    time.sleep(2)
    pyautogui.click(1460, 524)
    time.sleep(2)
    pyautogui.moveTo(1465, 450)
    pyautogui.dragTo(1465, 400, duration=1)
    time.sleep(2)
    pyautogui.click(1480, 590)
    time.sleep(2)

# Patient List 작업 및 텍스트 추출
def patient_list_cleanup():
    pyautogui.click(350, 70)
    time.sleep(2)
    pyautogui.moveTo(1304, 66)
    pyautogui.dragTo(1304, 895, duration=2.0)
    pyautogui.keyDown('shift')
    pyautogui.click(158, 902)
    pyautogui.keyUp('shift')
    time.sleep(2)
    pyautogui.click(1395, 215)
    time.sleep(2)
    number_extracted = extract_number_from_image(656, 436, 870, 470)
    print(f"Extracted number: {number_extracted}")

# 전체 작업 실행
def execute_all():
    main_workflow()
    patient_list_cleanup()

# 스크립트 실행
if __name__ == "__main__":
    time.sleep(2)  # 실행 전에 준비할 시간을 줍니다
    execute_all()
