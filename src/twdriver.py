import pickle

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from twexceptions import BotProtectionException
from twexceptions import SessionExpiredException


MAIN_URL = "https://www.plemiona.pl/"
DOMAIN = ".plemiona.pl"


class TWDriver(webdriver.Chrome):
    def __init__(self, world):
        webdriver.Chrome.__init__(self)
        self.world = world
        self.get(MAIN_URL)
        try:
            with open("cookies.pkl", "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    if cookie["domain"] == DOMAIN:
                        self.add_cookie(cookie)
            self.get(MAIN_URL + "page/play/" + self.world)
        except FileNotFoundError:
            pass

    def goto(self, query):
        self.get("https://" + self.world + DOMAIN + "/game.php?" + query)
        if self.element_exists_by_id("bot_check"):
            raise BotProtectionException
        if "session_expired=1" in self.current_url:
            raise SessionExpiredException

    def element_exists_by_id(self, id_):
        try:
            self.find_element_by_id(id_)
        except NoSuchElementException:
            return False
        else:
            return True

    def close(self):
        with open("cookies.pkl", "wb") as file:
            cookies = self.get_cookies()
            pickle.dump(cookies, file)
        webdriver.Chrome.close(self)
