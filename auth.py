
import requests, re, json, sys, os
from constants import *

def pre_auth():
    r = requests.get(page + '/enter');
    cookies = r.cookies
    body = r.text
    csrf = re.search('data-csrf=\'([0-9a-zA-Z]*)\'', body).group(1)
    r = requests.post(page + '/data/empty', cookies = cookies, data = {'ftaa': ftaa, 'bfaa': bfaa})
    cookies.update(r.cookies)
    return csrf, cookies, ftaa, bfaa

# Takes username and password and returns a cookie object 
def login(username, password):
    csrf, cookies, ftaa, bfaa = pre_auth()
    r = requests.post(page + '/enter', cookies = cookies, data = {
        'csrf_token': csrf,
        'bfaa': bfaa,
        'ftaa': ftaa,
        'action': 'enter',
        'handleOrEmail': username,
        'password': password
    })
    cookies.update(r.cookies)
    return requests.utils.dict_from_cookiejar(cookies)

def submit(problem, contest, solution, language, cookies):
    cookies = requests.utils.cookiejar_from_dict(cookies)
    url = page_http + '/contest/' + contest + '/submit'
    r = requests.get(url, cookies = cookies)
    csrf = re.search('data-csrf=\'([0-9a-zA-Z]*)\'', r.text).group(1)

    r = requests.post(url, cookies = cookies, data = {
        'csrf_token': csrf,
        'bfaa': bfaa,
        'ftaa': ftaa,
        'action': 'submitSolutionFormSubmitted',
        'contestId': contest,
        'submittedProblemIndex': problem,
        'programTypeId': language
        }, files = {'sourceFile': open(solution, 'rb')})
