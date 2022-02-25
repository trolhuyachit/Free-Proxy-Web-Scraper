import os, requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from sqlalchemy import false, true

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
options.add_experimental_option("excludeSwitches", ["enable-logging"])

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def scrapeProxiesSpy(url):
    urls = ["https://spys.one/en/free-proxy-list/", "https://spys.one/en/anonymous-proxy-list/", "https://spys.one/en/https-ssl-proxy/", "https://spys.one/en/socks-proxy-list/"]
    driver = webdriver.Chrome(options=options)
    for url in urls:
        driver.get(f"Loaded {url}")
        try: #Wait 10 seconds until the id we are looking for is found if not we close the driver
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "spy1")))
            print(f"Loaded spys.one")
            sleep(1)

            element = driver.find_element_by_id("xpp")
            drp = Select(element)
            sleep(1)
            drp.select_by_visible_text('500')
            #do it again cuz its wacko
            element = driver.find_element_by_id("xpp")
            drp = Select(element)
            sleep(1)
            drp.select_by_visible_text('500')

            print("Set Page Hight")
            sleep(8)

            proxies = {}
            all_proxies = driver.find_elements_by_class_name("spy14")
            for proxy in all_proxies:
                with open("proxies.txt", "a") as f:
                    if (not any(c.isalpha() for c in proxy.text)):
                        if proxy.text != "+":
                            f.write(f"{proxy.text}\n")
        finally:
            sleep(1)
            driver.quit()

def downloadProxies():
    urls = {"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all": "http_proxies.txt", 
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all" : "socks4_proxies.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all" : "socks5_proxies.txt"}

    for url, file in urls.items():
        print(f"Loaded {url}")
        r = requests.get(url, allow_redirects=True)
        open(file, 'wb').write(r.content)
        with open(file) as temp:
            with open("proxies.txt", "a") as f:
                for line in temp:
                    f.write(line)
        print(f"{file} coppied")
        os.remove(file)
        print(f"{file} cleaned")
        sleep(1)

def scrapeProxiesFree(url):
    urls = ["https://free-proxy-list.net/anonymous-proxy.html", "https://free-proxy-list.net/", "https://www.socks-proxy.net/", "https://www.sslproxies.org/"]
    driver = webdriver.Chrome(options=options)
    for url in urls:
        driver.get(url)
        try: #Wait 10 seconds until the id we are looking for is found if not we close the driver
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
            sleep(2)
            print(f"Loaded {url}")
            proxies = {}
            for i in range(101):
                if i > 0:
                    ip = driver.find_element_by_css_selector(f"#list > div > div.table-responsive > div > table > tbody > tr:nth-child({i}) > td:nth-child(1)")
                    port = driver.find_element_by_css_selector(f"#list > div > div.table-responsive > div > table > tbody > tr:nth-child({i}) > td:nth-child(2)")
                    proxies[ip.text]=port.text
            for ip, port in proxies.items():
                with open("proxies.txt", "a") as f:
                    f.write(f"{ip}:{port}\n")
        finally:
            sleep(1)
            driver.quit()

def scrapeProxiesLong(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try: #Wait 10 seconds until the id we are looking for is found if not we close the driver
        main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "clickexport")))
        print(f"Loaded {url}")

        ips = []
        all_proxies = driver.find_elements_by_class_name("left")
        for span in all_proxies:
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

        for ip, port in proxies.items():
            with open("proxies.txt", "a") as f:
                f.write(f"{ip}:{port}\n")
    finally:
        sleep(1)
        driver.quit()

def getProxiesLong(x):
    url = "http://free-proxy.cz/en/proxylist/main/"
    for i in range(x):
        scrapeProxiesLong(url + str(i))

def getProxies():
    scrapeProxiesSpy()
    scrapeProxiesFree()
    getProxiesLong(5)
    downloadProxies()


def getFileLength():
    file = open("proxies.txt", "r")
    nonempty_lines = [line.strip("\n") for line in file if line != "\n"]
    line_count = len(nonempty_lines)
    file.close()
    return(line_count)

if __name__ == "__main__":
    getProxies()
    print(f"{getFileLength()} Total Proxies")