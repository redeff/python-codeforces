import requests, re, concurrent.futures, os, webbrowser
from constants import *

def single_request(tag_url):
    return (tag_url[0], requests.get(tag_url[1]))

def bunch_of_requests(url_dict):
    out = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = [executor.submit(single_request, (a, b)) for a, b in url_dict.items()]
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            out[data[0]] = data[1]

    return out

def problem_given_page(location, contest, problem, page):
    # print(page.text)
    inp_regex = '<div class="input">\s*<div class="title">Input</div>\s*<pre>([\s\S]*?)</pre>\s*</div>'
    inp = map(lambda x: x.group(1), re.finditer(inp_regex, page))

    for i, val in enumerate(inp):
        with open(os.path.join(location, f'{i}.in'), "w+") as f:
            f.write(val)
   
    out_regex = '<div class="output">\s*<div class="title">Output</div>\s*<pre>([\s\S]*?)</pre>\s*</div>'
    out = map(lambda x: x.group(1), re.finditer(out_regex, page))

    for i, val in enumerate(out):
        with open(os.path.join(location, f'{i}.out'), "w+") as f:
            f.write(val)

def problem_page(contest, problem):
    return f'http://codeforces.com/contest/{contest}/problem/{problem}'

def problem(location, contest, problem):
    loc = os.path.join(location, contest, problem)
    os.makedirs(loc)
    problem_given_page(loc, contest, problem, requests.get(problem_page(contest, problem)).text)

def contest(location, contest):
    url = f'http://codeforces.com/contest/{contest}/problems'
    webbrowser.open(url, new=2)
    page = requests.get(url)
    parts = re.split('<div class="problemindexholder" problemindex="', page.text)[1:-1]

    for part in parts:
        problem = re.search('^[^"]*', part).group(0)
        loc = os.path.join(location, contest, problem)
        os.makedirs(loc)
        problem_given_page(loc, contest, problem, part)
