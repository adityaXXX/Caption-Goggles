import pprint
import zulip
import sys
import re
import json
import httplib2
import os
import math
import threading
from topnews import News
from meet import grouping

BOT_MAIL = "ghost-bot@zulipchat.com"

class Ghost(object):
    """
    Description of the bot
    """

    def __init__(self):
        self.client = zulip.Client(config_file="~/.zuliprc")
        self.subscribe_all()
        self.news = News()

    def subscribe_all(self):
        json = self.client.get_streams()["streams"]
        streams = [{"name": stream["name"]} for stream in json]
        self.client.add_subscriptions(streams)
    
    def process(self, msg):
        message_id = msg["id"]
        content  = msg["content"].split()
        sender_email = msg["sender_email"]
        
        stream_name = msg["display_recipient"]
        
        #print(content)
        #print(content[0],content[1])
        #if sender_email == BOT_MAIL:
        #    return
        if content[0].lower() == "@**ghost**":
            message = ""
            print("yes")
            if content[1].lower() == "hello" or content[1].lower() == "hi":
                message = "Hola"
            elif content[1].lower() == "news":
                try:
                    news = self.news.getTopNews()
                    for item in news:
                        message += "**"+item.title+"**"
                        message += '\n'
                        message += item.des
                        message += '\n\n'
                except:
                    message = "No news as of now ... try something like football"
            elif content[1].lower() == "meetup":
                name = ""
                for i in range(2,len(content)):
                    name += content[i]
                
                try:
                    dicti = grouping(name)
                    message += "Name: " + dicti["Name"] + '\n'
                    message += "Organizer: " + dicti["Organizer"] + '\n'
                    message += "City: " + dicti["City"] + '\n'
                    message += "Next Event: " + dicti["Upcoming Event"]["Event Name"] + '\n'
                    message += "RSVP: " + dicti["Upcoming Event"]["RSVP"] + '\n'
                    message += "Time: " + dicti["Upcoming Event"]["Time"] + '\n'
                    message += "Link: " + dicti["Upcoming Event"]["Link"] + '\n'
                except:
                    message = "Invalid Group Name"
            else:
                message += "Show top 10 news : **Ghost news**\n"
                message += "Show MeetUp group details and next event status"

            self.client.send_message({
                "type": "stream",
                "to": stream_name,
                "subject": msg["subject"],
                "content": message
            })

def main():
    gh = Ghost()
    gh.client.call_on_each_message(gh.process)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Adios")
        sys.exit(0)