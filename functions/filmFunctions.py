from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import re
import json
from bs4 import BeautifulSoup
from unidecode import unidecode
def parsehtml(html_content, file_path):
    soup = BeautifulSoup(html_content, 'html.parser')
    product_cards = soup.find('div', class_='c-productListings_grid g-grid-container u-grid-columns g-inner-spacing-bottom-large').find_all(
                        'div', class_='c-finderProductCard')
    href_values = [card.find('a')['href'] for card in product_cards]
    product_cards2 = soup.find('div', class_ = 'c-productListings_grid g-grid-container u-grid-columns g-inner-spacing-bottom-large g-inner-spacing-top-large').find_all(
        'div', class_='c-finderProductCard')
    href_values2 = [card.find('a')['href'] for card in product_cards2]
    href_values = href_values + href_values2
    href_values.append('\n')
    with open(file_path, 'a') as file:
        file.write('\n'.join(href_values))

def run(scroll_delay, output_file, template, ini, fini):
    links = geraLink(template, ini, fini)
    options = Options()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    q= 0
    driver = webdriver.Firefox(options=options)
    driver.get(links[q])
    try:
        while True:
            q +=1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_delay)

            current_height = driver.execute_script("return document.body.scrollHeight")
            window_height = driver.execute_script("return window.innerHeight")
            if current_height - window_height <= driver.execute_script("return window.scrollY"):
                parsehtml(driver.page_source, output_file)

                new_link = links[q]
                if not new_link:
                    break
                driver.get(new_link)
    except KeyboardInterrupt:
        pass
    finally:
        driver.quit()


def contaLinha(file_path, ):
    empty_line_count = 0
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.strip() == '':  # Check if the line is empty or contains only whitespace characters
            empty_line_count += 1  # Increment the counter
    print(f"Number of empty lines in the text file: {empty_line_count}, total = {len(lines)-empty_line_count}")

    return  empty_line_count

def geraLink(template, ini, fini):
    links = []
    for i in range(ini, fini + 1):
        pagina = i
        link = template + str(pagina)
        links.append(link)
    return links

def getMetascore(soup):
    try:
        div_element = soup.find('div', class_='c-siteReviewScore_background c-siteReviewScore_background-critic_large')
        span_element = div_element.find('span', {'data-v-4cdca868': True})
        metascore = span_element.text
    except:
        metascore = -1
    return metascore
def getUserscore(soup):
    try:
        div_element = soup.find('div', class_='c-siteReviewScore_background c-siteReviewScore_background-user')
        span_element = div_element.find('span', {'data-v-4cdca868': True})
        userscore = span_element.text
    except:
        userscore = -1
    return userscore

def getscorePositive(soup, classe):
    try:
        div_element = soup.find('div', class_=classe)
        #positives
        positive = div_element.find('div', class_= 'c-reviewsStats_positiveStats')
        spans = positive.find_all('span')
        span_texts = [span.get_text() for span in spans]
        positiveP = re.search(r'\d+', span_texts[0])
        positiveP = positiveP.group()
        positiveF = re.search(r'\d+', span_texts[1])
        positiveF = positiveF.group()
    except:
       positiveF = 0
       positiveP = 0
    #positiveP = porcentage
    #positiveF = flat number
    return positiveF, positiveP

def getscoreNegative(soup, classe):
    try:
        div_element = soup.find('div', class_=classe)
        negative = div_element.find('div', class_= 'c-reviewsStats_negativeStats')
        spans = negative.find_all('span')
        span_texts = [span.get_text() for span in spans]
        negativeP = re.search(r'\d+', span_texts[0])
        negativeP = negativeP.group()
        negativeF = re.search(r'\d+', span_texts[1])
        negativeF = negativeF.group()
    except:
       negativeF = 0
       negativeP = 0
    #negativeP = porcentage
    #negativeF = flat number
    return negativeF, negativeP

def getscoreMixed(soup, classe):
    try:
        div_element = soup.find('div', class_=classe)
        neutral = div_element.find('div', class_= 'c-reviewsStats_neutralStats')
        spans = neutral.find_all('span')
        span_texts = [span.get_text() for span in spans]
        neutralP = re.search(r'\d+', span_texts[0])
        neutralP = neutralP.group()
        neutralF = re.search(r'\d+', span_texts[1])
        neutralF = neutralF.group()
    except:
       neutralF = 0
       neutralP = 0
    #neutralP = porcentage
    #neutralF = flat number
    return neutralF, neutralP

def getAllScores(soup, mode):
    #user score
    if mode == 0:
        classe = 'c-reviewsSection_carouselContainer c-reviewsSection_carouselContainer-user'
    #meta score
    else:
        classe = 'c-reviewsSection_carouselContainer c-reviewsSection_carouselContainer-critic'
    num1, positive = getscorePositive(soup, classe)
    num3, mixed = getscoreMixed(soup, classe)
    num2, negative = getscoreNegative(soup,classe)
    return (int(num1) + int(num2) + int(num3)), positive, mixed, negative
def getTitle(soup):
    try:
        div_element = soup.find('div', class_='c-productHero_title g-inner-spacing-bottom-medium g-outer-spacing-top-medium')
        text = div_element.text
        text = text.rstrip()
        title = text.lstrip()
    except:
        title = ''
    return title

def getDirectors(soup):
    try:
        div_element = soup.find('div', class_='c-crewList g-inner-spacing-bottom-small c-productDetails_staff_directors')
        a_elements = div_element.find_all('a', class_='c-crewList_link u-text-underline')
        href_values = [a.get('href') for a in a_elements]
        director = []
        for values in href_values:
            parts = values.split('/')
            result = parts[-2]
            result = result.replace('-', ' ')
            director.append(result)
    except:
        director = ''
    return director

def getWriters(soup):
    try:
        writer = []
        div_element = soup.find('div', class_='c-crewList g-inner-spacing-bottom-small c-productDetails_staff_writers')
        a_elements = div_element.find_all('a', class_='c-crewList_link u-text-underline')
        href_values = [a.get('href') for a in a_elements]
        for values in href_values:
            parts = values.split('/')
            result = parts[-2]
            result = result.replace('-', ' ')
            writer.append(result)
    except:
        writer = ''
    return writer

def getCast(soup):
    try:
        cast = []
        div_element = soup.find('div', class_='c-globalCarousel_content c-globalCarousel_content-scrollable c-globalCarousel_content-scrollable_mobile-gap-small')
        a_elements = div_element.find_all('a', class_='c-globalPersonCard_container u-grid')
        href_values = [a.get('href') for a in a_elements]
        for values in href_values:
            parts = values.split('/')
            result = parts[-2]
            result = result.replace('-', ' ')
            cast.append(result)
    except:
        cast = ''
    return cast

def getDetails(soup):
    div_element = soup.find('div',
                            class_='c-movieDetails')
    span_elements = div_element.find_all('span', class_='g-outer-spacing-left-medium-fluid')
    span_elements2 = div_element.find_all('span', class_='g-text-bold')
    production_company = ''
    release_date = ''
    duration = ''
    rating = ''
    genres = ''
    tagline = ''
    website = ''
    for i in range(len(span_elements2)):
        text1_value = span_elements2[i].get_text(strip=True)
        try:
            text2 = span_elements[i].get_text(strip=True)
        except:
            text2 = ''

        # Check if the text1 value matches any criteria
        if "Production Company" == text1_value:
            production_company = text2
        elif "Release Date" == text1_value:
            release_date = text2
        elif "Duration" == text1_value:
            duration = text2
        elif "Rating" == text1_value:
            rating = text2
        elif "Genres" == text1_value:
            span_elements.insert(i, '')
            genres = []
            div_element = soup.find('div',
                                    class_='c-movieDetails_sectionContainer g-outer-spacing-top-small g-inner-spacing-medium u-flexbox u-flexbox-row u-flexbox-alignBaseline')
            span = div_element.find_all('span', class_='c-globalButton_label')
            for text in span:
                genres.append(text.get_text(strip=True))
        elif "Tagline" == text1_value:
            tagline = text2
        elif "Website" == text1_value:
            website = text2
    return production_company, release_date, duration, rating, genres, tagline,website

def getAwards(soup):
    try:
        awards = []
        div = soup.find_all(class_='c-productionAwardSummary_award')

        for award in div:
            title = award.find(class_='g-text-bold').get_text(strip=True)
            details = award.find_all('div')[1].get_text(strip=True)
            awards.append(title)
            awards.append(details)

    except:
        awards = ''
    return awards

def getSummary(soup):
    div_element = soup.find('div',
                            class_='c-productDetails g-inner-spacing-top-medium g-inner-spacing-bottom-large-fluid u-grid-columns c-productHero_details--desktop g-grid-container c-productDetails--desktop')
    span_element = div_element.find('span', class_= 'c-productDetails_description g-text-xsmall')
    summary = span_element.get_text(strip=True)
    return summary

def leFilme(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    metascore = getMetascore(soup)
    userscore = getUserscore(soup)
    title = getTitle(soup)
    director = getDirectors(soup)
    writer = getWriters(soup)
    cast = getCast(soup)
    production_company, release_date, duration, rating, genres, tagline, website = getDetails(soup)
    awards = getAwards(soup)
    summary = getSummary(soup)
    totalU, positiveU, mixedU, negativeU = getAllScores(soup, 0)
    totalM, positiveM, mixedM, negativeM = getAllScores(soup, 1)
    return metascore,userscore, title, director, writer, cast, production_company, release_date, duration, rating, genres, tagline, website, awards, summary, totalU, positiveU, mixedU, negativeU, totalM, positiveM, mixedM, negativeM



def getReviews(html_content):
    soup = BeautifulSoup(html_content,  'html.parser')
    div_elements = soup.find_all('div', class_='c-siteReview g-bg-gray10 u-grid g-outer-spacing-bottom-large')
    score = []
    plataforms = []
    date = []
    name = []
    review = []
    for item in div_elements:
        try:
            target_span = item.find('span', {'data-v-4cdca868': True})
            scr = target_span.get_text()
            score.append(scr)
        except:
            score.append('')
        try:
            target_a = item.find('a', class_='c-siteReviewHeader_username g-text-bold g-color-gray90')
            title = target_a.get_text()
            title = title.strip()
        except:
            try:
                target_a = item.find('a', class_='c-siteReviewHeader_publicationName g-text-bold g-color-gray90')
                title = target_a.get_text()
                title = title.strip()
            except:
                title = ''
        name.append(title)
        try:
            target_div = item.find('div', class_='c-siteReviewHeader_reviewDate g-color-gray80 u-text-uppercase')
            dt = target_div.get_text()
            dt = dt.strip()
        except:
            dt = ''
        date.append(dt)
        try:
            target_div = item.find('div', class_='c-siteReview_quote g-outer-spacing-bottom-small')
            target_span = target_div.find('span')
            rv = target_span.get_text()
            rv = rv.strip()
        except:
            rv = ''
        review.append(rv)
        try:
            target_div = item.find('div', class_='c-siteReview_platform g-text-bold g-color-gray80 g-text-xsmall u-text-right u-text-uppercase')
            plataform = target_div.get_text()
            plataform = plataform.strip()
        except:
            plataform = ''
        plataforms.append(plataform)
    return score, name, review, date, plataforms


def createJson(html_content):
    scores, names, reviews, dates, toxicity, language = getReviews(html_content)
    data = []
    for i in range(len(scores)):
        item = {
            "score": scores[i],
            "name": names[i],
            "review": reviews[i],
            "date": dates[i],
            "toxicity": toxicity[i],
            "language": language[i],
        }
        data.append(item)
    json_string = json.dumps(data)

    return json_string

def fazFilme(driver, link_list, ini, fini):
    max_scrolls = 15
    for i  in range(ini, fini+1):
        print(f'iteração {i} de {fini}')
        #generate the links
        try:
            movieLink = 'https://www.metacritic.com' + link_list[i]
            userLink =  movieLink +'user-reviews/'
            metaLink = movieLink + 'critic-reviews/'
            #get the movie main page
            driver.get(movieLink)
            time.sleep(0.25)
            metascore, userscore, title, director, writer, cast, production_company, release_date, duration, rating, genres, tagline, website, awards, summary, totalU, positiveU, mixedU, negativeU, totalM, positiveM, mixedM, negativeM = leFilme(driver.page_source)

            #get the user commentaries page
            driver.get(userLink)
            time.sleep(0.25)
            prev_height = 0
            if i < 100:
                for _ in range(max_scrolls):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.25)
                    current_height = driver.execute_script("return document.body.scrollHeight;")
                    if current_height == prev_height:
                        break
                    prev_height = current_height
            jsonUser = getReviews(driver.page_source)

            driver.get(metaLink)
            time.sleep(0.25)
            jsonMeta = getReviews(driver.page_source)
            metascore = unidecode(metascore)
            userscore = unidecode(userscore)
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
                "userReviews":jsonUser,
                "metaReviews":jsonMeta,
            }

            filename = "all_movie_data.json"
            with open(filename, "a", encoding="utf-8") as json_file:
                json_string = json.dumps(movie_data, ensure_ascii=False)
                json_file.write(json_string + ',' +'\n')
        except:
            continue

