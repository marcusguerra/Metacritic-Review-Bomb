from functions import ApiFunctions as api
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

link = 'https://www.metacritic.com/movie/vertigo-1958/'

options = Options()
options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
driver = webdriver.Firefox(options=options)

#modes: 0 get the comments; 1 dont get the comments

result = api.getData(driver, link,0)
print(result)