from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.utils import Singleton, EventListener


class SeleniumAgent(EventListener, metaclass=Singleton):

    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless=new")
        self.options.add_argument("--remote-debugging-port=9222")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-renderer-backgrounding")
        self.options.add_argument("--disable-background-timer-throttling")
        self.options.add_argument("--disable-backgrounding-occluded-windows")
        self.options.add_argument("--disable-client-side-phishing-detection")
        self.options.add_argument("--disable-crash-reporter")
        self.options.add_argument("--disable-oopr-debug-crash-dump")
        self.options.add_argument("--no-crash-upload")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-low-res-tiling")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("--silent")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        self.options.add_experimental_option("detach", True)
        self.dispatch("log_debug", "Setup Driver Options")

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.set_window_size(1920, 1080)
        self.subscribe("close_selenium", self.driver.quit)
        self.dispatch("log_debug", "Started Driver")

        self.dispatch("log_debug", "Attempting to navigate to 1337x")
        self.driver.get("https://duckduckgo.com/?origin=funnel_home_website&t=h_&q=1337x.to&ia=web")
        self.driver.execute_script("document.body.style.zoom='100%'")  # Triggers reflow
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # Scroll to bottom to trigger lazy loads
        try:
            self.dispatch("log_debug", "Waiting for page to load")
            wait = WebDriverWait(self.driver, 15)
            # wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            link_element = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "1377x | Download torrents")))

            self.dispatch("log_debug", "Searching for correct link")

            link_element = self.driver.find_element(By.PARTIAL_LINK_TEXT, "1377x | Download torrents")
            link_element.click()

            self.dispatch("log_debug", "Closing ads")
            input_field = self.driver.find_element(By.TAG_NAME, "input")
            input_field.click()
            self.close_popups()
            self.dispatch("log_debug", "Ready for input")
        except NoSuchElementException:
            self.dispatch("log_error", "No Element found")
            self.dispatch("log_error", "Dump: " + self.driver.page_source)
            self.driver.quit()
            self.dispatch("error_close")

        except TimeoutException:
            self.dispatch("log_error", "Request Timed Out")
            self.dispatch("log_error", "Dump: " + self.driver.page_source)
            self.driver.quit()
            self.dispatch("error_close")

    def close_popups(self):
        self.dispatch("log_debug", "Closing extra windows")
        first_window = self.driver.window_handles[0]
        for handle in self.driver.window_handles:
            if handle != first_window:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.driver.switch_to.window(first_window)

    def search(self, query):
        self.dispatch("log_info", "Running search on " + query)
        try:
            self.close_popups()
            element = self.driver.find_element(By.TAG_NAME, "input")
            element.clear()
            element.send_keys(query)
            element.submit()
            self.close_popups()
            self.dispatch("log_debug", "Waiting for page to load")
            wait = WebDriverWait(self.driver, 15)
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            self.dispatch("query_response", self.driver.page_source)
        except TimeoutException:
            self.dispatch("log_error", "Request Timed Out")
            self.driver.quit()
            self.dispatch("error_close")
