import requests, re, concurrent.futures, os, webbrowser
from constants import *

class Page:
    def __init__(self, text, contest):
        self.text = text
        self.contest = contest

    @classmethod
    def download(cls, contest, problem=None):
        url = ""
        if problem == None:
            url = f'http://codeforces.com/contest/{contest}/problems'
        else:
            url = f'http://codeforces.com/contest/{contest}/problem/{problem}'

        text = requests.get(url).text
        self = Page(text, contest)

        return self

    def testcases(self):
        inp_regex = '<div class="input">\s*<div class="title">Input</div>\s*<pre>([\s\S]*?)</pre>\s*</div>'
        inp = [x.group(1) for x in re.finditer(inp_regex, self.text)]
       
        out_regex = '<div class="output">\s*<div class="title">Output</div>\s*<pre>([\s\S]*?)</pre>\s*</div>'
        out = [x.group(1) for x in re.finditer(out_regex, self.text)]

        return Testcases(inp, out)

    def split(self):
        out = []

        parts = re.split('<div class="problemindexholder" problemindex="', self.text)[1:]
        for part in parts:
            problem = re.search('^[^"]*', part).group(0)
            out.append(Problem(self.contest, problem, Page(part, self.contest)))

        return out

class Problem:
    def __init__(self, contest, problem, page=None):
        self.contest = contest
        self.problem = problem
        if page == None:
            self.page = Page.download(contest, problem)
        else:
            self.page = page

    def testcases(self):
        return self.page.testcases()

    def save(self, location):
        loc = os.path.join(location, self.contest, self.problem)
        self.testcases().save(loc)

class Contest:
    def __init__(self, contest):
        self.contest = contest

    def save(self, location):
        page = Page.download(self.contest)
        problems = page.split()
        for problem in problems:
            problem.save(location)

class Testcases:
    def __init__(self, inp, out):
        self.inp = inp
        self.out = out

    def save(self, location):
        os.makedirs(location)
        for i, val in enumerate(self.inp):
            with open(os.path.join(location, f'{i}.in'), "w+") as f:
                f.write(val)

        for i, val in enumerate(self.out):
            with open(os.path.join(location, f'{i}.out'), "w+") as f:
                f.write(val)
