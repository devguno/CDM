import pyautogui
import time
import pyperclip
import pytesseract
from PIL import ImageGrab
import re
import os

# Set up the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Get age from clipboard
def get_age_from_clipboard():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    text = pyperclip.paste()
    try:
        return int(text.strip())
    except ValueError:
        return None

# Extract number from a specific screen region
def extract_number_from_image(x1, y1, x2, y2):
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    text = pytesseract.image_to_string(screenshot)
    numbers = re.findall(r'\d+', text)
    return int(numbers[0]) if numbers else None

# Perform basic clicks
def perform_basic_clicks():
    pyautogui.click(368, 950)
    time.sleep(2)
    pyautogui.click(1484, 88)
    time.sleep(2)
    pyautogui.click(1395, 167)
    time.sleep(2)
    pyautogui.click(1480, 77)
    time.sleep(2)

# Set Sinus Heart Rate based on lower and upper limits
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

# Perform initial click operations
def initial_clicks():
    # Click on Menu-System
    pyautogui.click(23, 35)
    time.sleep(2)
    
    # Click on Menu-System-System setup
    pyautogui.moveTo(63, 76)
    time.sleep(2)
    
    # Click on Menu-System-System setup-General
    pyautogui.click(231, 362)
    time.sleep(2)
    
    # Drag operation from (1260, 388) to (875, 388)
    pyautogui.moveTo(1260, 388)
    pyautogui.dragTo(875, 388, duration=1)
    time.sleep(2)
    
    # Extract the folder name from the last part of the path
    directory = "C:\\Holter"
    folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    print(f"Folder list: {folder_list}")
    
    for folder in folder_list:
        folder_path = os.path.join(directory, folder)
        folder_name = folder_path.split('\\')[-1]
        file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]) - 1
        
        iteration_count = 1
        for i in range(file_count):
            # Construct the file name using folder_name and iteration_count
            file_name = f"{folder_name}_{iteration_count}"
            
            # Click on 'Patient Information'
            pyautogui.click(215, 955)
            time.sleep(2)
            
            # Copy data for further processing
            pyautogui.click(1050, 87)
            pyautogui.dragTo(910, 87, duration=1)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(2)
            
            # Get the copied text and append it to the file name
            clipboard_text = pyperclip.paste()
            full_file_name = f"{file_name}_{clipboard_text}"
            
            # Here, you would save the file with `full_file_name`
            print(f"Full file name: {full_file_name}")
            
            iteration_count += 1

# Main workflow based on age
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

# Patient list cleanup and number extraction
def patient_list_cleanup():
    time.sleep(2)
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
    time.sleep(2)
    pyautogui.click(1000, 460)  # Click No
    time.sleep(2)
    return number_extracted

# Save patient data
def save_patient_data(total_pages):
    for _ in range(total_pages):
        pyautogui.moveTo(570, 125)
        pyautogui.dragTo(640, 125, duration=1)
        time.sleep(2)
        pyautogui.click(320, 898)
        pyautogui.click(1560, 124)
        pyautogui.click(1480, 218)
        time.sleep(2)
        # Simulate file save operation
        pyautogui.click(23, 35)  # Click on Menu-System
        time.sleep(2)
        pyautogui.moveTo(63, 76)  # Click on Menu-System-System setup
        time.sleep(2)
        pyautogui.click(231, 362)  # Click on General setup
        pyautogui.dragTo(875, 388, duration=1)
        time.sleep(2)

# Execute all operations
def execute_all():
    main_workflow()
    extracted_number = patient_list_cleanup()
    if extracted_number:
        total_pages = extracted_number // 56
        save_patient_data(total_pages)
    process_folder_data()

# Run the script
if __name__ == "__main__":
    time.sleep(2) 
    execute_all()
