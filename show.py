import sys
import random
import json
from flask import Flask, render_template

app = Flask(__name__)

with open('options.json') as fo:
    options = json.load(fo)
    print(options)


def sentenceCapitaliser(para):
    sentences = para.split(". ")
    sentences2 = [sentence[0].capitalize() + sentence[1:]
                  for sentence in sentences]
    string2 = '. '.join(sentences2)
    return string2


def pick(filler):
    opts = options[filler]
    chosen = random.randrange(0, len(opts))
    return opts[chosen]

def fillBlanks(para, char1):
    desc = para.format(place=pick("place"),
                       char1=char1[0],
                       forms=char1[1],
                       relationship=pick("relationship"),
                       char2=pick("char2"),
                       char2_possession=pick("char2_possession"),
                       mission=pick("mission"),
                       shared_interest=pick("shared_interest"),
                       historic_element=pick("historic_element"),
                       historic_where=pick("historic_where"),
                       action=pick("action"),
                       final=pick("final"),
                       firstname=pick("firstname"),
                       surname=pick("surname"))
    return desc


@app.route('/')
def gen_show():
    title = pick("title")
    char1 = pick("char1")
    para = pick("para")
    desc = fillBlanks(para, char1)
    return render_template("index.html", title=title.upper(), desc=sentenceCapitaliser(desc))


if __name__ == "__main__":
    app.run()
