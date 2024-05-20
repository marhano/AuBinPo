import pyautogui
import time

def idle(interval, duration):
    time.sleep(5)
    print("Starting idle mode...")
    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            pyautogui.click()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Idle mode stopped.")

interval = 10
duration = 3600

idle(interval, duration)