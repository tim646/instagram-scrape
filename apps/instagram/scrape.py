import json
import os
import time
import urllib.request
from datetime import datetime

from bs4 import BeautifulSoup
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from apps.instagram.models import InstagramPost, InstagramScrape


#
#
def extract_plain_text(html_string):
    """Extracts plain text from html string. Removes all html tags. Used for extracting post text."""
    soup = BeautifulSoup(html_string, "html.parser")
    plain_text = soup.get_text()
    return plain_text.strip()


#
def extract_json_data(driver, json_xpath):
    """Extracts the JSON data from the given XPath."""
    json_element = driver.find_element(By.XPATH, json_xpath)
    json_text = json_element.get_attribute("text")
    json_data = json.loads(json_text)
    return json_data


def extract_likes_count(json_data):
    """Extracts the likes count from the JSON data."""
    interaction_statistics = json_data.get("interactionStatistic", [])
    for stat in interaction_statistics:
        if stat.get("@type") == "InteractionCounter" and stat.get("interactionType") == "http://schema.org/LikeAction":
            likes_count = stat.get("userInteractionCount", 0)
            return likes_count
    return 0


def extract_post_text(json_data):
    description = json_data.get("articleBody", "")
    return extract_plain_text(description)


def extract_published_date(json_data):
    date_published = json_data.get("dateCreated", "")
    date = datetime.strptime(date_published, "%Y-%m-%dT%H:%M:%S%z")

    return date.date()


def web_scraping():
    """Scrapes instagram posts from a given account. Saves posts to database, if they exist in database, it updates
    the function gets the posts likes, text, image, link and created day."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--window-size=1200,900")
    options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    scrape_info = InstagramScrape.get_solo()

    if scrape_info is not None:
        username = driver.find_element(By.XPATH, "//input[@name='username']")
        username.clear()
        username.send_keys(scrape_info.username)

        password = driver.find_element(By.XPATH, "//input[@name='password']")
        password.clear()
        password.send_keys(scrape_info.password)

        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        time.sleep(5)

        try:
            not_now_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            not_now_button.click()
        except Exception as e:
            pass

        try:
            not_now_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            not_now_button.click()
        except Exception as e:
            pass

        driver.get(f"https://www.instagram.com/{scrape_info.target_username}/")
        time.sleep(5)

        n_scrolls = 1
        for _ in range(n_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

        anchors = driver.find_elements(By.TAG_NAME, "a")
        anchors = [a.get_attribute("href") for a in anchors]
        print(f"\n\n\n{len(anchors)}\n\n\n")

        parent_dir = os.path.join(settings.MEDIA_ROOT, "instagram")
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        for i, a in enumerate(anchors):
            print(f"\n\n\n{i} {a}\n")
            if str(a).startswith("https://www.instagram.com/p/"):
                time.sleep(1)
                # print(a)
                post_url = a.split("/p/")[-1].split("/")[0]
                print(post_url)
                img_url = f"https://www.instagram.com/p/{post_url}/media/?size=l"
                urllib.request.urlretrieve(img_url, os.path.join(parent_dir, f"{post_url}.jpg"))

                url = f"https://www.instagram.com/p/{post_url}/liked_by/"
                driver.get(url)
                time.sleep(5)

                json_xpath = "//script[contains(text(), 'userInteractionCount')]"
                json_data = extract_json_data(driver, json_xpath)

                try:
                    post_text = extract_post_text(json_data)
                except Exception as e:
                    print(f"Error extracting post text: {e}")
                    try:
                        driver.get(a)
                        time.sleep(5)
                        post_text_element = driver.find_element(
                            By.XPATH,
                            "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul/div/li/div/div/div[2]/div[1]/h1",
                        )
                        post_text_html = post_text_element.get_attribute("innerHTML")
                        post_text = extract_plain_text(post_text_html)
                    except Exception as e:
                        print(f"Error extracting post text: {e}")
                        post_text = ""
                try:
                    likes_count = extract_likes_count(json_data)
                except Exception as e:
                    print(f"Error extracting likes count: {e}")
                    try:
                        driver.get(url)
                        time.sleep(5)
                        likes = driver.find_elements(By.XPATH, '//button[@class="_acan _acap _acas _aj1-"]')
                        likes_count = len(likes)
                    except Exception as e:
                        print(f"Error extracting likes count: {e}")
                        likes_count = 0

                try:
                    published_date = extract_published_date(json_data)
                except Exception as e:
                    print(f"Error extracting published date: {e}")
                    try:
                        driver.get(a)
                        time.sleep(5)
                        date_element = driver.find_element(
                            By.XPATH,
                            "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[2]/div/a/span/time",
                        )
                        date_string = date_element.get_attribute("datetime")
                        published_date_format = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
                        published_date = published_date_format.strftime("%Y-%m-%d")
                    except Exception as e:
                        print(f"Error extracting date posted: {e}")
                        published_date = datetime.now().strftime("%Y-%m-%d")
                driver.back()
                obj, _ = InstagramPost.objects.get_or_create(
                    link=a,
                    image=f"instagram/{post_url}.jpg",
                    text=post_text,
                    likes=likes_count,
                    created_day=published_date,
                )

    driver.quit()
