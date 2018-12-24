#!/usr/bin/env python3
import requests, re, json, sys, os
import auth, do

def infer_from_extension(path):
    lala, ext = os.path.splitext(path)
    if ext == '.cpp':
        return 42
    else:
        print(ext)
        raise

if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help' or sys.argv[1] == 'help':
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
    print(json.dumps(auth.login(sys.argv[2], sys.argv[3])))
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
        language = 42 # code for c++17, the default language
    auth.submit(sys.argv[3], sys.argv[2], sys.argv[4], language, cookies)
elif sys.argv[1] == 'do':
    cwd = os.getcwd()
    if len(sys.argv) < 4:
        do.contest(cwd, sys.argv[2])
    else:
        do.problem(cwd, sys.argv[2], sys.argv[3])
else:
    raise
