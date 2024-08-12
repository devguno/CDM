import os
import pyautogui
import time
import pyperclip
import pytesseract
from PIL import ImageGrab
import re
from PIL import ImageEnhance, ImageOps

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
directory = pyperclip.paste()

# Strip unwanted characters or spaces from the text
directory = directory.strip()

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

# Loop through each file
for i in range(file_count):
    # Click 'Patient Select'
    pyautogui.click(140, 950)
    time.sleep(2)

    # Set y-coordinate
    y_coord = 71
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

    # Create the file name
    file_name = f"{folder_name}_{pid}"

    # Print or save the file_name
    print(f'Generated File Name: {file_name}')

    # Update y_coord for the next iteration 
    y_coord += 15  

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
