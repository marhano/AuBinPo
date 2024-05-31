import pyautogui
import time

def auto_scroll(interval=1, duration=60, scroll_down_amount=-100, scroll_up_amount=100, scroll_up_interval=600):
    """
    Automatically scrolls down the screen and scrolls up at specified intervals.
    
    :param interval: Time between scroll down actions in seconds.
    :param duration: Total time to scroll in seconds.
    :param scroll_down_amount: Amount to scroll down. Negative value.
    :param scroll_up_amount: Amount to scroll up. Positive value.
    :param scroll_up_interval: Time interval to trigger scroll up in seconds.
    """
    start_time = time.time()
    last_scroll_up_time = start_time
    
    while time.time() - start_time < duration:
        current_time = time.time()
        
        # Scroll down at regular intervals
        pyautogui.scroll(scroll_down_amount)
        time.sleep(interval)
        
        # Scroll up every `scroll_up_interval` seconds
        if current_time - last_scroll_up_time >= scroll_up_interval:
            pyautogui.scroll(scroll_up_amount)
            last_scroll_up_time = current_time

# Example usage: Scroll down every 1 second for a total of 60 seconds, scroll up every 10 minutes
auto_scroll(interval=5, duration=7200, scroll_down_amount=-100, scroll_up_amount=10000, scroll_up_interval=300)