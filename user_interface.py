import requests
import os
import json
import time


class UserInterface():

    user = None
    logged_in = False
    on = True

    @classmethod
    def log_in(cls):

        os.system('clear')
        print("Welcome to Tweetcool!")
        action = input("Log in as: ")
        if action == 'x' or action == 'X':
            cls.on = False
        else:
            cls.user = action
            cls.logged_in = True

    def __init__(self, user, address):

        self.name = user
        self.server = address

    def run(self):

        while self.__class__.logged_in:
            os.system('clear')
            r = requests.get(self.server + '/tweet', {'offset' : 10 })
            all_messages = r.json()
            for msg in all_messages:
                time_to_display = str(time.ctime(msg["timestamp"]))
                print(msg["poster"] + " posted at " + time_to_display + " >>> " + msg["content"])
            action = input("\n\nPOST SOMETHING NOW!\n('x' quits)\n" + self.name + " >>> ")
            if action == 'x':
                self.__class__.logged_in = False
            elif action == 'X':
                self.__class__.logged_in = False
                self.__class__.on = False
            else:
                tweet = {"poster": self.name, "content": action}
                x = requests.post(self.server + '/tweet', json=tweet)
