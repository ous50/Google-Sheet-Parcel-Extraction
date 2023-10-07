import json
import requests
from urllib.parse import quote_plus

def send_bark(msg):

    # Read configuration from config.json
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    bark_url = config.get("bark", {}).get("url")
    title = config.get("bark", {}).get("title")

    # For cases that the bark_url is not set in config.json:
    if not bark_url:
        print("bark_url not set in config.json, please set it to use bark notification.")
        return
    
    # print(config.get("bark", {}))
    # For cases that the title is not set in config.json:
    if not title:
        print("title not set in config.json, using default title.")
        title = "Package Notification"
        url = bark_url + title + "/" + quote_plus(msg) + "\n Your Title is not set. \n" + "Set the 'title' in config.json to customize."
    else:
        url = bark_url + title + "/" + quote_plus(msg)

    requests.get(url)