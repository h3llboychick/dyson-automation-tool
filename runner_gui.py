import tkinter as tk
from tkinter import ttk
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
import os
from fake_useragent import UserAgent
from random import randint
import multiprocessing
import psutil


ua = UserAgent()

def initialize_driver():
    #Creating Chromium browser instance

    #Adding options to avoid detection
    chromium_options = ChromeOptions()
    chromium_options.add_argument("--disable-blink-features=AutomationControlled")
    chromium_options.add_argument(f"--user-agent={ua.getBrowser('chrome')}")
    chromium_options.add_argument('--disable-gpu')
    chromium_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    chromium_options.add_experimental_option("useAutomationExtension", False)

    #Path to Chromium
    browser_binary_location = "C:\\AutomationScript\\chromium\\Chrome-bin\\chrome.exe"

    #Checking whether is chromium installed or not
    if not os.path.isfile(browser_binary_location):
        return None
    chromium_options.binary_location = browser_binary_location

    chromium_driver_path = "C:\\AutomationScript\\chromedriver\\chromedriver.exe"

    service = Service(chromium_driver_path)

    #Creaint Chromium Instance
    return webdriver.Chrome(service = service, options = chromium_options)

def check_dyson(dyson_login, dyson_password, done_event):

    #Function to scroll any given page for the number of pixels(step) and for a certain number of iteration(number)
    def make_scrolling(driver, number, step):
        stopScrolling = 0
        while True:
            stopScrolling += 1
            driver.execute_script(f"window.scrollBy(0,{step})")
            time.sleep(0.5)
            if stopScrolling > number:
                break
        driver.execute_script("window.scrollTo(0,0)")

    #Function to go back to dyson.com's main page
    def back_to_the_main_page(wait):
        back_to_the_main_page = wait.until(
            EC.visibility_of_element_located((
                By.XPATH, 
                '//a[@data-analytics-nav-type="logo"]'
        )))
        back_to_the_main_page.click()
    
    #Open hamburger menu on dyson.com main page
    def go_hamburger(driver, wait):
        hamburger_menu = wait.until(
            EC.element_to_be_clickable((
                By.XPATH, 
                '//button[@aria-controls="primary-nav"]'
        )))
        ActionChains(driver).move_to_element(hamburger_menu).click(hamburger_menu).perform()

    #Function to avoid being detected by anti-bot system
    def avoid_detection(driver, wait):
        deals_page = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//a[@data-analytics-nav-name="deals"]'
            )))

        deals_page.click()

        wait.until(
            EC.visibility_of_element_located((
                By.XPATH, 
                '//li[@role="group"]'
        )))

        deals = driver.find_elements(By.XPATH, '//li[@role="group"]')
        for deal in deals:
            deal.click()
            make_scrolling(driver, 5, 150)

        back_to_the_main_page(wait)

        hair_care_page = wait.until(
            EC.visibility_of_element_located((
                By.XPATH, 
                '//a[@data-analytics-nav-name="vacuum cleaners"]'
        )))

        hair_care_page.click()
        make_scrolling(driver, 10, 150)

        back_to_the_main_page(wait)

        headphones_page = wait.until(
            EC.visibility_of_element_located((
                By.XPATH, 
                '//a[@data-analytics-nav-name="headphones"]'
        )))
        headphones_page.click()
        make_scrolling(driver, 10, 150)

        back_to_the_main_page(wait)


    driver = initialize_driver()

    if isinstance(driver, webdriver.Chrome):
        try:
            #Fetching browser instance
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
            driver.maximize_window()
            driver.get("https://dyson.com/en")

            wait = WebDriverWait(driver, 40)


            
            #STEP 1 & 2 Log in/out functionality + avoding detection (for long runs)

            avoid_detection(driver, wait)
            log_in_element = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//a[@data-analytics-nav-name="sign in / join"]'
            )))
            time.sleep(randint(2,5))

            log_in_element.click()

            log_in_button = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//button[@data-analytics-action-name="button~log in to mydyson™"]'
            )))

            email_input = driver.find_element(By.XPATH, '//input[@id="login-email"]')
            password_input = driver.find_element(By.XPATH, '//input[@id="password"]')

            email_input.send_keys(dyson_login)

            time.sleep(randint(1, 5))

            password_input.send_keys(dyson_password)

            time.sleep(randint(1, 5))

            ActionChains(driver).move_to_element(log_in_button).click(log_in_button).perform()

            log_out_button = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//button[@data-analytics-nav-type="log out"]'
            )))

            log_out_button.click()
            back_to_the_main_page(wait)

            #STEP 3 Exploring pages
            deals_page = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//a[@data-analytics-nav-name="deals"]'
            )))

            deals_page.click()

            wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//li[@role="group"]'
            )))

            deals = driver.find_elements(By.XPATH, '//li[@role="group"]')
            for deal in deals:
                deal.click()
                make_scrolling(driver, 5, 150)

            back_to_the_main_page(wait)

            hair_care_page = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//a[@data-analytics-nav-name="vacuum cleaners"]'
            )))

            hair_care_page.click()
            make_scrolling(driver, 10, 150)

            back_to_the_main_page(wait)

            headphones_page = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//a[@data-analytics-nav-name="headphones"]'
            )))
            headphones_page.click()
            make_scrolling(driver, 10, 150)

            back_to_the_main_page(wait)

            lightning_page = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//a[@data-analytics-nav-name="lighting"]'
            )))
            lightning_page.click()
            make_scrolling(driver, 10, 150)

            back_to_the_main_page(wait)
            go_hamburger(driver, wait)

            vacuum_cleaners_hamburger = wait.until(EC.element_to_be_clickable((
                By.XPATH, 
                '//div[@class= "hamburger-item__block"]/a[@data-analytics-nav-name="vacuum cleaners"]'
            )))
            vacuum_cleaners_hamburger.click()
            make_scrolling(driver, 10, 150)
            back_to_the_main_page(wait)
            go_hamburger(driver, wait)

            headphones_hamburger = wait.until(EC.element_to_be_clickable((
                By.XPATH, 
                '//div[@class= "hamburger-item__block"]/a[@data-analytics-nav-name="headphones"]'
            )))
            headphones_hamburger.click()
            make_scrolling(driver, 10, 150)
            back_to_the_main_page(wait)
            go_hamburger(driver, wait)

            lightning_hamburger = wait.until(EC.element_to_be_clickable((
                By.XPATH, 
                '//div[@class= "hamburger-item__block"]/a[@data-analytics-nav-name="lighting"]'
            )))
            lightning_hamburger.click()
            make_scrolling(driver, 10, 150)
            back_to_the_main_page(wait)
            go_hamburger(driver, wait)

            air_treatment_hamburger = wait.until(EC.element_to_be_clickable((
                By.XPATH, 
                '//div[@class= "hamburger-item__block"]/a[@data-analytics-nav-name="air treatment"]'
            )))
            air_treatment_hamburger.click()
            make_scrolling(driver, 10, 150)
            back_to_the_main_page(wait) 

            #STEP 4 User adding product to the basket
            go_hamburger(driver, wait)

            air_treatment_hamburger = wait.until(EC.element_to_be_clickable((
                By.XPATH, 
                '//div[@class= "hamburger-item__block"]/a[@data-analytics-nav-name="air treatment"]'
            )))
            air_treatment_hamburger.click()

            all_air_treatment_page = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//a[@data-analytics-action-name="textlink~shop all air purifier deals"]'
            )))

            all_air_treatment_page.click()

            add_to_basket_button = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//button[@data-analytics-action-name="cta~add to basket"]'
            )))

            add_to_basket_button.click()

            secure_checkout = secure_checkout = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//a[@data-analytics-action-name="text link~secure checkout"]'
            )))

            time.sleep(randint(1, 5))
            secure_checkout.click()

            wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//div[@data-analytics-action-title="your details"]'
            )))

            driver.find_element(By.XPATH, "//a[@class='header__logo']").click()
            
            #STEP 5 User adding a spare part/accesory to basket
            go_hamburger(driver, wait)
            spare_parts = wait.until(
            EC.element_to_be_clickable((
                By.XPATH, 
                '//a[@data-analytics-nav-name="parts and accessories"]'
            )))
            ActionChains(driver).move_to_element(spare_parts).click(spare_parts).perform()

            hair_care_section = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//button[@data-analytics-action-name="tile~hair care"]'
            )))
            hair_care_section.click()

            hair_styler_section = secure_checkout = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//button[@data-analytics-action-name="tile~hair stylers"]'
            )))
            hair_styler_section.click()

            airwarp_section = secure_checkout = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//button[@data-analytics-action-name="tile~dyson airwrap™ multi-styler"]'
            )))
            airwarp_section.click()

            cases_stands_section = secure_checkout = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//button[@data-analytics-action-name="tile~cases, stands and all other spare parts"]'
            )))
            cases_stands_section.click()

            accessories = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//span[@class="accordion-span"]'
            )))
            accessories = driver.find_elements(By.XPATH, '//span[@class="accordion-span"]')

            for accessory in accessories:
                accessory.click()
                accessory_wait = WebDriverWait(driver, 10)
                try:
                    button = accessory_wait.until(
                        EC.element_to_be_clickable((
                        By.XPATH, 
                        '//button[@data-analytics-action-name="cta~add to basket"]'
                    )))
                    button.click()
                except Exception:
                    continue

            secure_checkout = secure_checkout = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//a[@data-analytics-action-name="text link~secure checkout"]'
            )))
            secure_checkout.click()

            wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '//div[@data-analytics-action-title="your details"]'
            )))

            time.sleep(randint(1, 5))
            driver.close()
            driver.quit()
        except (NoSuchWindowException, AttributeError):
            driver.quit()
            return "Browser has been closed while script was running."
        except WebDriverException as e:
            driver.close()
            driver.quit()
            if "net::ERR_INTERNET_DISCONNECTED" in str(e):
                print("No internet connection.")
        except Exception as e:
            driver.close()
            driver.quit()
            print(f"Unknwon error occured: {str(e)}")
        finally:
            done_event.set()
    else:
        print("Error occured while launching browser instance. Check Chromium and chromedriver.exe installation.")

#Function to kill chromium and chromdriver.exe processing after clicking on stop
def kill_chromium_processes():
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            # Check if the process is a Chromium process (based on description or other criteria)
            if 'chromedriver' in proc.info['name'] or (proc.info.get("cmdline") and 'chromium' in proc.info.get("cmdline")[0]):
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
class ProgramGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dyson Automation Controller")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.interval = 0  # Default interval in seconds
        self.running = False
        self.done_event = multiprocessing.Event()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding=(100, 20))
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Create widgets
        self.hours_label = ttk.Label(root, text="Hours:")
        self.hours_label.pack(pady=5)

        self.email_label = ttk.Label(self.main_frame, text="Email:")
        self.email_label.pack(pady=5)
        
        self.email_variable = tk.StringVar()
        self.email_entry = ttk.Entry(self.main_frame, textvariable = self.email_variable)
        self.email_entry.pack(pady=5)

        self.password_label = ttk.Label(self.main_frame, text="Password:")
        self.password_label.pack(pady=5)
        
        self.password_variable = tk.StringVar()
        self.password_entry = ttk.Entry(self.main_frame, textvariable= self.password_variable)
        self.password_entry.pack(pady=5)

        self.hours_variable = tk.StringVar()
        self.hours_entry = ttk.Entry(root, textvariable = self.hours_variable)
        self.hours_variable.set("0")
        self.hours_entry.pack(pady=5)
        
        self.minutes_label = ttk.Label(root, text="Minutes:")
        self.minutes_label.pack(pady=5)
        
        self.minutes_variable = tk.StringVar()
        self.minutes_entry = ttk.Entry(root, textvariable = self.minutes_variable)
        self.minutes_variable.set("0")
        self.minutes_entry.pack(pady=5)
        
        self.seconds_label = ttk.Label(root, text="Seconds:")
        self.seconds_label.pack(pady=5)
        
        self.seconds_variable = tk.StringVar()
        self.seconds_entry = ttk.Entry(root, textvariable = self.seconds_variable)
        self.seconds_variable.set("0")
        self.seconds_entry.pack(pady=5)
        
        self.start_button = ttk.Button(root, text="Start", command=self.start_execution)
        self.start_button.pack(pady=5)
        
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_execution)
        self.stop_button.pack(pady=5)
        
        self.status_label = ttk.Label(root, text="Status: Stopped")
        self.status_label.pack(pady=10)
        
        self.time_left_label = ttk.Label(root, text="")
        self.time_left_label.pack(pady=10)
        
    def start_execution(self):
        try:
            hours = int(self.hours_variable.get())
            minutes = int(self.minutes_variable.get())
            seconds = int(self.seconds_variable.get())
            self.interval = hours * 3600 + minutes * 60 + seconds
            if self.interval <= 0:
                self.status_label.config(text="Status: Interval must be greater than 0")
                return
        except ValueError:
            self.status_label.config(text="Status: Invalid interval")
            self.hours_variable.set("0")
            self.minutes_variable.set("0")
            self.seconds_variable.set("0")
            return
        self.email = self.email_variable.get()
        self.password = self.password_variable.get()
        if not self.email or not self.password:
            self.status_label.config(text="Status: Please enter email and password")
            return
        self.done_event.clear()
        self.running = True
        self.status_label.config(text=f"Status: Running every {hours} hours, {minutes} minutes, {seconds} seconds")
        self.run_program()
    
    def stop_execution(self):
        self.done_event.clear()
        self.running = False
        kill_chromium_processes()
        self.process.terminate()
        self.process.join()
        self.status_label.config(text="Status: Stopped")
        self.time_left_label.config(text = "")
    
    def run_program(self):
        if not self.running:
            return
        self.done_event.clear()
        self.process = multiprocessing.Process(target=check_dyson, args=(self.email, self.password, self.done_event))
        self.process.start()
        self.countdown(self.interval)
        
    def countdown(self, t):
        if not self.running:
            return
        if self.done_event.is_set():
            mins, secs = divmod(t, 60)
            hours, mins = divmod(mins, 60)
            time_format = f'Time left: {hours:02d}:{mins:02d}:{secs:02d}'
            self.time_left_label.config(text=time_format)
            if t < 0:
                self.time_left_label.config(text = "")
                self.run_program()
            else:
                self.root.after(1000, self.countdown, t - 1)
        else:
            self.root.after(1000, self.countdown, t)
    
    def on_closing(self):
        self.stop_execution()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramGUI(root)
    root.mainloop()