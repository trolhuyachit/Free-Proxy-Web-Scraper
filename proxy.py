import os
import winsound
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def scrapeFreeProxycz(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=OFF")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    try: #Wait 10 seconds until the id we are looking for is found if not we close the driver
        main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "clickexport")))
        print("Loaded Fresh Proxy List")

        ips = []
        all_left = driver.find_elements_by_class_name("left")
        for span in all_left:
            if (not any(c.isalpha() for c in span.text)):
                ips.append(span.text)

        proxies = {}

        ports = []
        all_fport = driver.find_elements_by_class_name("fport")
        for port in all_fport:
            if (not any(c.isalpha() for c in port.text)):
                ports.append(port.text)
        
        for i in range(len(all_fport)):
            proxies[ips[i]]=ports[i]
        
        f = open("proxies.txt","a")
        for key, value in proxies.items():
            f.write("{}:{}\n".format(key, value))

    finally:
        driver.quit()

def getFreeProxycz(x):
    url = "http://free-proxy.cz/en/proxylist/main/"
    for i in range(x):
        scrapeFreeProxycz(url + str(i))

if __name__ == "__main__":
    getFreeProxycz(5)
    