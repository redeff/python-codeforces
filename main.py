#!/usr/bin/env python3
import requests, re, json, sys, os

# These are random numbers. It doesn't matter what they are,
# only that they're constant

# 18-digit base-36 random number
ftaa = 'bnh5yzdirjinqaorq0'

# 32-digit base-16 random number
bfaa = '1a55b95112dd900a28d64e2d0f841341'

page = 'https://codeforces.com'
page_http = 'http://codeforces.com'

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

def infer_from_extension(path):
    lala, ext = os.path.splitext(path)
    if ext == '.cpp':
        return 42
    else:
        print(ext)
        raise

if len(sys.argv) < 5 or sys.argv[1] == '-h' or sys.argv[1] == '--help' or sys.argv[1] == 'help':
    print("""Usage:

            login <username> <password>
            Outputs credentials through stdout

            -- or --

            submit <contest> <problem> <path/to/solution> [<language-code>]
            Receives credentials through stdin
            If language code is omitted, it'll be assumed to be c++17
            If language code is "_", it will be inferred from the file extension
            """)

elif sys.argv[1] == 'login':
    print(json.dumps(login(sys.argv[2], sys.argv[3])))
elif sys.argv[1] == 'submit':
    cookies = json.loads(sys.stdin.read())
    print("submitting...")
    language = 42
    if len(sys.argv) > 5:
        if sys.argv[5] == '_':
            language = infer_from_extension(sys.argv[4])
        else:
            language = sys.argv[5]
    else:
        language = 42
    submit(sys.argv[3], sys.argv[2], sys.argv[4], language, cookies)
else:
    raise
