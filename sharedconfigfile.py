import json
import vdfparser

from scrapper import SteamStoreScrapper

TAGS_PREFIX = ' '
TAGS_TAG = 'Tag: '
TAGS_YEAR = 'Year: '
TAGS_RATING = 'Rating: '


class SharedConfigFile():
    TAGS_KEY_TAGS = 'tags'

    def __init__(self, file):
        self.file = file
        self.vdf = vdfparser.parse(file)
        self.apps = self.vdf['UserRoamingConfigStore']['Software']['Valve']['Steam']['apps']  # NOQA

    def __str__(self):
        return vdfparser.serialize(self.vdf)

    def clear_all_tags(self):
        for appid in self.apps:
            if self.is_favorite(appid):
                self.apps[appid][self.TAGS_KEY_TAGS] = {'0': 'favorite'}
            else:
                self.apps[appid].pop(self.TAGS_KEY_TAGS, None)

    def is_favorite(self, appid):
        try:
            tags = self.apps[appid][self.TAGS_KEY_TAGS]
            for tagid in tags:
                if tags[tagid] == 'favorite':
                    return True
            return False
        except KeyError:
            return False

    def has_tags(self, appid):
        try:
            self.apps[appid][self.TAGS_KEY_TAGS]
            return True
        except KeyError:
            return False

    def clear_tags(self, app):
        try:
            for tag in self.apps[app][self.TAGS_KEY_TAGS]:
                print(tag)
        except KeyError:
            # This app had no tags
            pass

    def add_tag(self, appid, tag):
        if self.has_tags(appid):
            tags = self.apps[appid][self.TAGS_KEY_TAGS]
            next_idx = str(len(tags))
        else:
            next_idx = '0'
            self.apps[appid][self.TAGS_KEY_TAGS] = {}
            tags = self.apps[appid][self.TAGS_KEY_TAGS]
        tags[next_idx] = tag

    def normalize_rating(self, rating):
        if type(rating) is int:
            rating = rating // 10
            if rating == 10:
                rating = str(rating)
            else:
                rating = "{0}-{1}".format(rating * 10, rating * 10 + 9)
        return str(rating)

    def generate_game_tags(self, appid):
        try:
            data = self.fetch_game_data(appid)
            if data is None:
                print("The appid {0} doesn't seem to be a proper Steam store game.".format(appid))  # NOQA
                return
            if len(data['tags']) < 1:
                print("No tags found for {0} (appid:{1}), \
                    you might want to delete the JSON file.".format(
                    data['name'], appid)
                )
                return
            for tag in data['tags']:
                self.add_tag(appid, "{0}{1}{2}".format(
                    TAGS_PREFIX,
                    TAGS_TAG,
                    tag
                ))
            self.add_tag(appid, "{0}{1}{2}".format(
                TAGS_PREFIX,
                TAGS_YEAR,
                data['year']
            ))
            self.add_tag(appid, "{0}{1}{2}".format(
                TAGS_PREFIX,
                TAGS_RATING,
                self.normalize_rating(data['score'])
            ))
            # TODO add verbosity parameter
            print("{0}: Done.".format(data['name']))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except KeyError as e:
            print(">>>>>>>>>>")
            print("An error occured while scrapping appid {0}".format(appid))
            print("Here is the app's data so far:")
            print(data)
            print("Error data:")
            print(e)
            print("<<<<<<<<<<")

    def generate_all_tags(self):
        print("About to update tags for {0} games".format(len(self.apps)))
        for appid in self.apps:
            self.generate_game_tags(appid)

    def save_game_data(self, appid, data):
        f = open('json/{0}.json'.format(appid), 'w')
        json.dump(data, f)
        f.close()
        pass

    def fetch_game_data(self, appid):
        # TODO rework this with a better code style/meaning
        try:
            f = open('json/{0}.json'.format(appid), 'x')
            scr = SteamStoreScrapper()
            data = scr.scrap(appid)
            self.save_game_data(appid, data)
        except FileExistsError:
            # Data is already present, it can be loaded directly
            f = open('json/{0}.json'.format(appid), 'r')
            data = json.load(f)
        return data
