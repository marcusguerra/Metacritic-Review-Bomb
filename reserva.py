from functions import filmFunctions as ftfrom functions import gameFunctions as gffrom selenium import webdriverfrom selenium.webdriver.firefox.options import Optionsimport requestsfrom bs4 import BeautifulSoupurl = 'https://www.metacritic.com/game/shiken-yasumi-wa-mitsu-no-aji/'headers = {    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}''''options = Options()options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"driver = webdriver.Firefox(options=options)driver.get(link)max_scrolls = 15prev_height = 0for _ in range(max_scrolls):    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")    time.sleep(2)    current_height = driver.execute_script("return document.body.scrollHeight;")    if current_height == prev_height:        break    prev_height = current_height'''''# Send an HTTP request to the URLresponse = requests.get(url, headers=headers)if response.status_code == 200:    html_content = response.textelse:    print(f"Failed to retrieve the page. Status code: {response.status_code}")print(gf.leGame(html_content))