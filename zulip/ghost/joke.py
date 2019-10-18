import requests

def lame_jokes():
    url = "https://official-joke-api.appspot.com/random_joke"
    res = requests.get(url)
    req = res.json()
    setup = req['setup']
    pl = req['punchline']
    message = setup + '\n' + "**Punchline: **" + pl

    return message
