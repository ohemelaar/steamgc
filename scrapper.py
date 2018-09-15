import requests
import urllib
from bs4 import BeautifulSoup
import http.cookiejar
import re


class SteamStoreScrapper():
    STORE_HOMEPAGE = 'https://store.steampowered.com/'
    STORE_URL = STORE_HOMEPAGE + 'app/{0}'

    def __init__(self):
        pass

    def scrap(self, appid):
        soup = self.get_soup(appid)
        if soup is not None:
            name = self.get_name(soup)
            tags = self.get_tags(soup)
            score = self.get_score(soup)
            year = self.get_year(soup)
            data = {
                'name': name,
                'tags': tags,
                'score': score,
                'year': year,
            }
        else:
            data = None
        return data

    def get_past_age_check(self, url):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cj)
        )
        # GET the original url, it should return the page with the age form
        response = opener.open(url)
        sessionid = re.search(
            r'.*sessionid=(?P<sessionid>[0-9a-f]*).*',
            str(response.headers)
        ).group('sessionid')
        # Creating POST data
        data = urllib.parse.urlencode({
            'ageDay': '1',
            'ageMonth': 'January',
            'ageYear': '1954',
            'sessionid': sessionid,
            'snr': '1_agecheck_agecheck__age-gate',
        })
        data = data.encode('utf-8')
        url = response.url
        # POST on the page with the age form
        response = opener.open(url, data)
        # TODO check form post success
        return response

    def get_soup(self, appid):
        url = self.STORE_URL.format(appid)
        cookies = dict(mature_content='1')
        response = requests.get(url, cookies=cookies)
        if str(appid) not in response.url:
            return None
        elif response.url.find('agecheck') != -1:
            # There is another type of age check that is more difficult to pass
            response = self.get_past_age_check(url)
            # We are using two different type of response objects
            # because it's the only way I've found to pass the age check
            # So the methods to get the text are different
            # TODO : find a solution to use either urllib or responses
            # but not both
            soup = BeautifulSoup(response.read(), 'lxml')
        else:
            soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def get_name(self, soup):
        name = soup.find('title').get_text().strip()[:-9]
        return name

    def get_score(self, soup):
        score = soup.find(class_='score')
        if score is None:
            return 'Not rated'
        else:
            return score.get_text().strip()

    def get_year(self, soup):
        date = soup.find(class_='release_date')
        if date is None:
            return 'Unknown'
        else:
            date = date.get_text().strip()
            return date[-4:]

    def get_tags(self, soup):
        # soup = self.get_soup(appid)
        tags = list(map(
            lambda x: x.get_text().strip(),
            soup.find_all(class_='app_tag')
        ))
        # Sometimes there's a '+' in the tags list
        # I don't know why, let's remove it
        tags = list(filter(lambda x: x != '+', tags))
        return tags
