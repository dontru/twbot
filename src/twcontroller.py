import random
import time

from twdriver import TWDriver
from twexceptions import BotProtectionException
from twexceptions import SessionExpiredException


class TWController:
    def __init__(self, world):
        self.driver = TWDriver(world)

    def run(self):
        while True:
            command = input("--> ")
            words = command.split()

            try:
                if words[0] == "exit":
                    self.driver.close()
                    break
                elif words[0] == "farm":
                    self.farm(*[int(_) for _ in words[1:]])
            except BotProtectionException:
                print("bot protection")
            except SessionExpiredException:
                print("session expired")

    def farm(self, a=0, b=0, repeat=0):
        print(time.ctime())
        self.driver.goto("screen=am_farm")
        for i in range(0, a):
            self.driver.send_units(i, "A")
            self.sleep()
        for i in range(a, a + b):
            self.driver.send_units(i, "B")
            self.sleep()
        if repeat != 0:
            self.sleep(60 * repeat)
            self.farm(a, b, repeat)

    def sleep(self, secs=1):
        time.sleep(secs * random.uniform(0.8, 1.2))
