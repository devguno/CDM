import os
import pyautogui
import time
import pyperclip
import pytesseract
from PIL import ImageGrab
import re
from PIL import ImageEnhance, ImageOps

# Initialize iteration count
iteration_count = 1

time.sleep(2)

# Activate fail-safe (program stops if the mouse moves to the top left corner of the screen)
pyautogui.FAILSAFE = True

# Set up the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Click on Menu-System
pyautogui.click(23, 35)
time.sleep(2)

# Click on Menu-System-System setup
pyautogui.moveTo(63, 76)
time.sleep(2)

# Click on Menu-System-System setup-General
pyautogui.click(231, 362)
time.sleep(2)

# Drag from (1260, 388) to (875, 388)
pyautogui.moveTo(1260, 388)
pyautogui.dragTo(875, 388, duration=2)

# Perform the copy operation (Ctrl+C)
pyautogui.hotkey('ctrl', 'c')
time.sleep(1)  # Wait a moment for the text to be copied

# Get the copied text from the clipboard
directory = pyperclip.paste().strip()

# Extract the folder name from the directory
folder_name = directory.split('\\')[-1]

# Count the number of files in the directory
try:
    files = os.listdir(directory)
    file_count = len(files) - 1  # Subtract 1 from the total file count
except FileNotFoundError:
    print("The directory was not found.")
    file_count = 0

# Print the initial results
print(f'Extracted Directory: {directory}')
print(f'Folder Name: {folder_name}')
print(f'File Count (minus one): {file_count}')

# Set y-coordinate
y_coord = 71
time.sleep(2)

# Loop through each file
for i in range(file_count):
    # Click 'Patient Select'
    pyautogui.click(140, 950)
    time.sleep(2)

    # Click on patient from the list
    pyautogui.click(210, y_coord)
    time.sleep(2)

    # Click 'Patient Information'
    pyautogui.click(215, 955)
    time.sleep(2)

    # Select and copy patient ID
    pyautogui.click(1050, 87)
    pyautogui.dragTo(910, 87, duration=1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)

    # Get the patient ID from the clipboard
    pid = pyperclip.paste().strip()

    # OCR for the exam date
    date_image = ImageGrab.grab(bbox=(1040, 616, 1170, 640))
    date_text = pytesseract.image_to_string(date_image).strip()

    # Convert date to desired format YYYYMMDD
    match = re.search(r'(\d{2})-(\w{3})-(\d{4})', date_text)
    if match:
        day, month, year = match.groups()
        months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                  'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        hookupdate = f"{year}{months[month]}{day}"
    else:
        hookupdate = None

    print(f'Extracted Date: {hookupdate}')

    # OCR for the exam time
    time_image = ImageGrab.grab(bbox=(1020, 660, 1160, 690))

    # Convert to grayscale
    time_image = time_image.convert('L')

    # Increase contrast
    enhancer = ImageEnhance.Contrast(time_image)
    time_image = enhancer.enhance(2)  # Increase contrast

    # Optional: Invert colors if needed (for dark text on light background)
    time_image = ImageOps.invert(time_image)

    # Resize the image to improve OCR accuracy
    time_image = time_image.resize((time_image.width * 2, time_image.height * 2))

    # OCR
    time_text = pytesseract.image_to_string(time_image, config='--psm 7').strip()

    # Convert time to desired format HHMMSS
    match = re.search(r'(\d{2}):(\d{2}):(\d{2})', time_text)
    if match:
        hour, minute, second = match.groups()
        hookuptime = f"{hour}{minute}{second}"
    else:
        hookuptime = None

    print(f'Extracted Time: {hookuptime}')

    # Create the file name
    file_name = f"{folder_name}_{iteration_count}_{pid}_{hookupdate}_{hookuptime}"

    # Print or save the file_name
    print(f'Generated File Name: {file_name}')

    # Update y_coord for the next iteration 
    y_coord += 15  

    # Get age from the screen
    time.sleep(2)
    pyautogui.moveTo(640, 125)
    pyautogui.dragTo(570, 125, duration=1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    age = pyperclip.paste().strip()

    # Convert age to integer
    try:
        age = int(age)
    except ValueError:
        age = None

    # Set Sinus Heart Rate based on age
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

    def perform_basic_clicks():
        pyautogui.click(368, 950)
        time.sleep(2)
        pyautogui.click(1484, 88)
        time.sleep(2)
        pyautogui.click(1395, 167)
        time.sleep(2)
        pyautogui.click(1480, 77)
        time.sleep(2)

    if age == 0:
        perform_basic_clicks()
        set_sinus_heart_rate(100, 180)
    elif 1 <= age <= 5:
        perform_basic_clicks()
        set_sinus_heart_rate(70, 160)
    elif 5 <= age <= 10:
        perform_basic_clicks()
        set_sinus_heart_rate(65, 140)
    elif 10 <= age <= 15:
        perform_basic_clicks()
        set_sinus_heart_rate(60, 130)
    elif age > 15:
        perform_basic_clicks()
        set_sinus_heart_rate(60, 100)

    pyautogui.click(1460, 507)
    time.sleep(2)
    pyautogui.click(1460, 524)
    time.sleep(2)
    pyautogui.moveTo(1465, 450)
    pyautogui.dragTo(1465, 400, duration=1)
    time.sleep(2)
    pyautogui.click(1480, 590)
    time.sleep(2)

    # Extract the number of pages or items
    pyautogui.click(350, 70)
    time.sleep(2)
    pyautogui.moveTo(1304, 66)
    pyautogui.dragTo(1304, 895, duration=2.0)
    pyautogui.keyDown('shift')
    pyautogui.click(158, 902)
    pyautogui.keyUp('shift')
    time.sleep(2)
    #click Delete
    pyautogui.click(1395, 215)
    time.sleep(2)

    def extract_number_from_image(x1, y1, x2, y2):
        number_image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        number_image = number_image.convert('L')
        enhancer = ImageEnhance.Contrast(number_image)
        number_image = enhancer.enhance(2)
        number_image = number_image.resize((number_image.width * 2, number_image.height * 2))
        number_text = pytesseract.image_to_string(number_image, config='--psm 7').strip()
        number = int(re.sub(r'\D', '', number_text))  # Extract only digits
        return number

    number_extracted = extract_number_from_image(656, 436, 870, 470)
    print(f"Extracted number: {number_extracted}")
    time.sleep(2)
    # Click No
    pyautogui.click(1000, 460)  
    time.sleep(2)
    # Perform the drag in reverse direction
    pyautogui.moveTo(1304, 895)
    pyautogui.dragTo(1304, 66, duration=2.0)
    time.sleep(3)

    # Calculate total pages
    total_pages = number_extracted // 56
    print(f"total_pages: {total_pages}")

    # Loop through each page
    for page in range(1, total_pages + 1):  # Start range from 1 to total_pages inclusive
        # Update file_name with the current page number
        updated_file_name = f"{file_name}_{page}"
        
        pyautogui.click(700, 896)
        time.sleep(2)
        
        if page > 1:
            pyautogui.press('pagedown')
            time.sleep(2)
        
        pyautogui.click(1540, 120)
        time.sleep(2)
        
        pyautogui.click(1500, 225)
        time.sleep(2)
        
        pyperclip.copy(updated_file_name)  # Copy the updated file name to clipboard
        pyautogui.hotkey('ctrl', 'v')  # Paste the updated file name
        time.sleep(2)
        
        pyautogui.click(1080, 680)  # Confirm
        time.sleep(5)

    # Increment the iteration count after processing all pages
    iteration_count += 1
