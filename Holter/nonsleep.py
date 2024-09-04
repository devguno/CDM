import pyautogui
import time

# Coordinates for the clicks
coord1 = (1440, 1050) 
coord2 = (1460, 1050)

# Time between clicks
delay_between_clicks = 200  # 5 minutes in seconds

# Two weeks in seconds
two_weeks_seconds = 2 * 7 * 24 * 60 * 60

# Start time
start_time = time.time()

while time.time() - start_time < two_weeks_seconds:
    # First click
    pyautogui.click(coord1)
    time.sleep(delay_between_clicks)
    
    # Second click
    pyautogui.click(coord2)
    time.sleep(delay_between_clicks)
