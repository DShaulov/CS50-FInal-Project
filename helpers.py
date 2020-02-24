import requests
import json
from flask import session, redirect

def lookup(word):

    app_key = "0e2ad71d68e3053d83f5c0d682c08c71"
    app_id = "8567b8d2"

    endpoint = "entries"
    language_code = "en-us"
    word_id = word

    url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + word_id.lower()

    r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key}).json()

    definitions = r["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"]
    return definitions
