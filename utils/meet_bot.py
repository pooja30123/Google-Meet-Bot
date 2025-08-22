from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from utils.audio_recorder import AudioRecorder
import time
import config

class GoogleMeetBot:
    def __init__(self):
        self.browser = None
        self.audio_recorder = None
        self.meeting_is_active = False
        
    def setup_browser(self):
        browser_options = Options()
        browser_options.add_experimental_option("detach", True)
        browser_options.add_argument("--use-fake-ui-for-media-stream")
        browser_options.add_argument("--start-maximized")
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--disable-dev-shm-usage")
        
        media_permissions = {
            "profile.default_content_setting_values": {
                "media_stream_mic": 1,
                "media_stream_camera": 1,
                "notifications": 2
            }
        }
        browser_options.add_experimental_option("prefs", media_permissions)
        
        try:
            print("Setting up Chrome browser...")
            chrome_service = Service(ChromeDriverManager(driver_version="139.0.7258.80").install())
            self.browser = webdriver.Chrome(service=chrome_service, options=browser_options)
            
            self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome setup successful")
            return True
            
        except Exception as error:
            print("Chrome setup failed, trying fallback...")
            try:
                chrome_service = Service(ChromeDriverManager().install())
                self.browser = webdriver.Chrome(service=chrome_service, options=browser_options)
                self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                print("✅ Fallback Chrome working")
                return True
            except Exception as fallback_error:
                print(f"Both attempts failed: {fallback_error}")
                return False
    
    def join_meeting(self, meeting_url):
        if not self.setup_browser():
            return False
        
        try:
            print(f"Opening meeting: {meeting_url}")
            self.browser.get(meeting_url)
            time.sleep(8)
            
            print("Configuring audio and video...")
            
            self.turn_off_microphone()
            self.turn_off_camera()
            
            print("Looking for join button...")
            join_successful = self.attempt_to_join()
            
            if join_successful:
                print("✅ Meeting joined successfully")
                self.meeting_is_active = True
                time.sleep(5)
                return True
            else:
                print("Join attempt completed")
                self.meeting_is_active = True
                return True
                
        except Exception as error:
            print(f"Meeting join failed: {error}")
            return False
    
    def turn_off_microphone(self):
        microphone_selectors = [
            '[aria-label*="microphone"]',
            '[aria-label*="Turn off microphone"]',
            '[data-testid*="mic"]',
            'div[aria-label*="Mute"]'
        ]
        
        for selector in microphone_selectors:
            try:
                mic_button = self.browser.find_element(By.CSS_SELECTOR, selector)
                if mic_button.is_displayed():
                    mic_button.click()
                    print("Microphone disabled")
                    time.sleep(1)
                    break
            except:
                continue
    
    def turn_off_camera(self):
        camera_selectors = [
            '[aria-label*="camera"]',
            '[aria-label*="Turn off camera"]',
            '[data-testid*="camera"]',
            'div[aria-label*="camera off"]'
        ]
        
        for selector in camera_selectors:
            try:
                camera_button = self.browser.find_element(By.CSS_SELECTOR, selector)
                if camera_button.is_displayed():
                    camera_button.click()
                    print("Camera disabled")
                    time.sleep(1)
                    break
            except:
                continue
    
    def attempt_to_join(self):
        join_button_options = [
            ("XPATH", "//span[contains(text(), 'Join now')]"),
            ("XPATH", "//span[contains(text(), 'Ask to join')]"),
            ("XPATH", "//div[contains(text(), 'Join now')]"),
            ("CSS", "[data-testid='join-button']"),
            ("CSS", "button[jsname='Qx7uuf']")
        ]
        
        for search_method, selector in join_button_options:
            try:
                if search_method == "XPATH":
                    join_button = self.browser.find_element(By.XPATH, selector)
                else:
                    join_button = self.browser.find_element(By.CSS_SELECTOR, selector)
                
                if join_button.is_displayed() and join_button.is_enabled():
                    join_button.click()
                    print(f"Clicked join button using: {selector}")
                    return True
            except:
                continue
        
        print("Join button not found, trying Enter key")
        self.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.ENTER)
        time.sleep(2)
        return False
    
    def start_recording(self, session_name):
        if not self.meeting_is_active:
            print("No active meeting to record")
            return False
        
        try:
            print(f"Starting audio recording: {session_name}")
            self.audio_recorder = AudioRecorder()
            recording_started = self.audio_recorder.start_recording(session_name, config.RECORDINGS_DIR)
            
            if recording_started:
                print("✅ Recording started")
                return True
            else:
                print("Recording failed to start")
                return False
                
        except Exception as error:
            print(f"Recording error: {error}")
            return False
    
    def stop_recording(self):
        if self.audio_recorder:
            print("Stopping recording...")
            audio_file_path = self.audio_recorder.stop_recording()
            print(f"Recording saved: {audio_file_path}")
            return audio_file_path
        return None
    
    def leave_meeting(self):
        print("Leaving meeting...")
        try:
            self.find_and_click_leave_button()
        except Exception as error:
            print(f"Could not leave gracefully: {error}")
        
        finally:
            if self.browser:
                self.browser.quit()
                print("Browser closed")
                self.meeting_is_active = False
    
    def find_and_click_leave_button(self):
        leave_button_selectors = [
            '[aria-label*="Leave call"]',
            '[data-testid*="leave"]',
            'button[aria-label*="Leave call"]'
        ]
        
        for selector in leave_button_selectors:
            try:
                leave_button = self.browser.find_element(By.CSS_SELECTOR, selector)
                if leave_button.is_displayed():
                    leave_button.click()
                    print("Left meeting via button")
                    break
            except:
                continue
