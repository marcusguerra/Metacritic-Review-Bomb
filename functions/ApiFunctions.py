from functions import filmFunctions as ft
from functions import gameFunctions as gt
from unidecode import unidecode
import json
import time

def getGame(driver, link, comentaries = 0):
    max_scrolls = 100

    # generate the links
    gameLink = link
    userLink = gameLink + 'user-reviews/'
    metaLink = gameLink + 'critic-reviews/'
    try:
        # get the movie main page
        html_content = gt.tryBS4(gameLink)
        metascore, userscore, platafoms, title, rating, release_date, dev, publisher, genres, totalU, positiveU, mixedU, negativeU, totalM, positiveM, mixedM, negativeM = gt.leGame(
            html_content)

        if ((metascore == -1 and userscore == -1) or comentaries == 1):
            jsonUser = ft.getReviews(html_content)
            jsonMeta = ft.getReviews(html_content)

        else:
            # get the user commentaries page
            driver.get(userLink)
            time.sleep(0.25)
            prev_height = 0
            for _ in range(max_scrolls):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.2)
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

        json_string = json.dumps(game_data, ensure_ascii=False)
        return json_string

    except Exception as e:
        print(f"An error occurred: {e}")

def getMovie(driver, link, comentaries = 0):
    max_scrolls = 100

    # generate the links
    movieLink = link
    userLink = movieLink + 'user-reviews/'
    metaLink = movieLink + 'critic-reviews/'
    try:
        # get the movie main page
        html_content = gt.tryBS4(movieLink)
        metascore, userscore, title, director, writer, cast, production_company, release_date, duration, rating, genres, tagline, website, awards, summary, totalU, positiveU, mixedU, negativeU, totalM, positiveM, mixedM, negativeM = ft.leFilme(html_content)

        if ((metascore == -1 and userscore == -1) or comentaries == 1):
            jsonUser = ft.getReviews(html_content)
            jsonMeta = ft.getReviews(html_content)

        else:
            # get the user commentaries page
            driver.get(userLink)
            time.sleep(0.25)
            prev_height = 0
            for _ in range(max_scrolls):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.2)
                current_height = driver.execute_script("return document.body.scrollHeight;")
                if current_height == prev_height:
                    break
                prev_height = current_height
            jsonUser = ft.getReviews(driver.page_source)
            driver.get(metaLink)
            time.sleep(0.25)
            jsonMeta = ft.getReviews(driver.page_source)
        title = unidecode(title)
        director = [unidecode(actor) for actor in director]
        writer = [unidecode(actor) for actor in writer]
        cast = [unidecode(actor) for actor in cast]
        release_date = unidecode(release_date)
        duration = unidecode(duration)
        rating = unidecode(rating)
        genres = [unidecode(genre) for genre in genres]
        tagline = unidecode(tagline)
        website = unidecode(website)
        awards = [unidecode(genre) for genre in awards]
        summary = unidecode(summary)

        movie_data = {
            "metascore": metascore,
            "userscore": userscore,
            "title": title,
            "director": director,
            "writer": writer,
            "cast": cast,
            "production_company": production_company,
            "release_date": release_date,
            "duration": duration,
            "rating": rating,
            "genres": genres,
            "tagline": tagline,
            "website": website,
            "awards": awards,
            "summary": summary,
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

        json_string = json.dumps(movie_data, ensure_ascii=False)
        return json_string

    except Exception as e:
        print(f"An error occurred: {e}")

def getData(driver = '', url = '', comentaries = 0):
    parts = url.split('/')
    type = parts[-3]
    if(type == 'game'):
        return getGame(driver, url, comentaries)
    elif(type == 'movie'):
        return getMovie(driver, url, comentaries)
    else:
        print('link not found')