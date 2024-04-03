from functions import filmFunctions as ft
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import json
from bs4 import BeautifulSoup
from unidecode import unidecode
def leGame(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    metascore = ft.getMetascore(soup)
    userscore = getUserscore(soup)
    title = ft.getTitle(soup)
    rating = getRating(soup)
    platafoms = getPlataforms(soup)
    date, dev, publisher, genres = getDetails(soup)
    totalU, positiveU, mixedU, negativeU = ft.getAllScores(soup, 0)
    totalM, positiveM, mixedM, negativeM = ft.getAllScores(soup, 1)
    return metascore, userscore, platafoms, title, rating, date, dev, publisher, genres, totalU, positiveU, mixedU, negativeU, totalM, positiveM, mixedM, negativeM

def getUserscore(soup):
    try:
        div_element = soup.find('div', class_='c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green c-siteReviewScore_user g-color-gray90 c-siteReviewScore_large')
        span_element = div_element.find('span', {'data-v-4cdca868': True})
        userscore = span_element.text
    except:
        userscore = -1
    return userscore
def getRating(soup):
    try:
        div_element = soup.find('div', class_ = 'c-productionDetailsGame_esrb_title u-inline-block g-outer-spacing-left-medium-fluid')
        span_element = div_element.find('span', class_= 'u-block')
        rating = span_element.get_text(strip=True)
        rating = rating.split()[-1]
    except:
        rating = ''
    return rating

def getPlataforms(soup):
    platforms =[]
    try:
        div_element = soup.find('div', class_='c-gameDetails_Platforms u-flexbox u-flexbox-row')
        li_element = div_element.find_all('li', class_='c-gameDetails_listItem g-color-gray70 u-inline-block')
        for li in li_element:
            platforms.append(li.get_text(strip=True))
    except:
        return platforms
    return platforms

def getDetails(soup):
    try:
        div_element = soup.find('div', class_='c-gameDetails_ReleaseDate u-flexbox u-flexbox-row')
        span_element = div_element.find('span', class_='g-outer-spacing-left-medium-fluid g-color-gray70 u-block')
        date = span_element.get_text(strip=True)
    except:
        date = ''

    dev =[]
    try:
        div_element = soup.find('div', class_='c-gameDetails_Developer u-flexbox u-flexbox-row')
        li_elements = div_element.find_all('li', class_='c-gameDetails_listItem g-color-gray70 u-inline-block')
        for li in li_elements:
            dev.append(li.get_text(strip=True))
    except:
        dev = ''
    publisher = []
    try:
        div_element = soup.find('div', class_='c-gameDetails_Distributor u-flexbox u-flexbox-row')
        span_element = div_element.find_all('span', class_='g-outer-spacing-left-medium-fluid g-color-gray70 u-block')
        for span in span_element:
            publisher.append(span.get_text(strip=True))
    except:
        publisher = ''
    genres = []
    try:
        div_element = soup.find('li',
                                class_='c-genreList_item')
        span = div_element.find_all('span', class_='c-globalButton_label')
        for text in span:
            genres.append(text.get_text(strip=True))
    except:
        genres = ''
    return date, dev, publisher, genres

def tryBS4(link):
    url = link
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    return html_content

#metascore, userscore, platafoms, title, rating, date, dev, publisher, genres, totalU, positiveU, mixedU, negativeU, totalM, positiveM, mixedM, negativeM
def fazJogo(driver, link_list, ini, fini):
    max_scrolls = 100

    for i  in range(ini, fini+1):
        print(f'iteração {i} de {fini}')
        #generate the links
        movieLink = 'https://www.metacritic.com' + link_list[i]
        userLink = movieLink + 'user-reviews/'
        metaLink = movieLink + 'critic-reviews/'
        try:
            #get the movie main page
            html_content =  tryBS4(movieLink)
            metascore, userscore, platafoms, title, rating, release_date, dev, publisher, genres, totalU, positiveU, mixedU, negativeU, totalM, positiveM, mixedM, negativeM = leGame(html_content)

            if(metascore == -1 and userscore == -1):
                jsonUser = ft.getReviews(html_content)
                jsonMeta = ft.getReviews(html_content)

            else:
            #get the user commentaries page
                driver.get(userLink)
                time.sleep(0.25)
                prev_height = 0
                for _ in range(max_scrolls):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.2)
                    current_height = driver.execute_script("return document.body.scrollHeight;")
                    if current_height == prev_height:
                        break
                    prev_height = current_height
                jsonUser = ft.getReviews(driver.page_source)

                driver.get(metaLink)
                time.sleep(0.25)
                jsonMeta = ft.getReviews(driver.page_source)
            title = unidecode(title)
            plataforms = [unidecode(actor) for actor in platafoms]
            release_date = unidecode(release_date)
            rating = unidecode(rating)
            dev = [unidecode(genre) for genre in dev]
            genres = [unidecode(genre) for genre in genres]
            publisher = [unidecode(genre) for genre in publisher]
            game_data = {
                "metascore": metascore,
                "userscore": userscore,
                "platforms": plataforms,
                "title": title,
                "rating": rating,
                "release_date": release_date,
                "developer": dev,
                "publisher": publisher,
                "genres": genres,
                "user_reviews": {
                    "total": totalU,
                    "positive": positiveU,
                    "mixed": mixedU,
                    "negative": negativeU
                },
                "metacritic_reviews": {
                    "total": totalM,
                    "positive": positiveM,
                    "mixed": mixedM,
                    "negative": negativeM
                },
                "userReviews": jsonUser,
                "metaReviews": jsonMeta,
            }

            filename = "all_games_data.json"
            with open(filename, "a", encoding="utf-8") as json_file:
                json_string = json.dumps(game_data, ensure_ascii=False)
                json_file.write(json_string + ',' +'\n')
        except Exception  as e:
            print(f"An error occurred: {e}")
            continue

