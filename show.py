import random
import json
import shutil
import time
import glob
import os
import sys
from flask import Flask, render_template, request, redirect, url_for
sys.path.insert(0, os.path.basename(__file__))
import forms

app = Flask(__name__)
app.config["SECRET_KEY"] = "blarrghhdshsg"


def loadOptions():
    jo = (app.root_path + "/options.json")
    with open(jo, encoding="utf-8") as fo:
        global options
        options = json.load(fo)


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


def dictToString(options):
    newDict = {}
    for k in options.keys():
        newstr = ""
        for o in options[k]:
            newstr = newstr + str(o) + "\n"
        newDict[k] = newstr
    return newDict


def marshalFormData(data):
    new_dict = {}
    for k in data.keys():
        if k in ["csrf_token", "f_submit"]:
            continue  # we don't need this
        options = data[k].split("\r\n")
        options = [x for x in options if x != '']
        if k == "f_char1":
            for i in range((len(options)-1), 0, -1):
                options[i] = eval(options[i])
        new_dict[k[2:]] = options
    return new_dict


def backupOptions():
    src = (app.root_path + "/options.json")
    t = str(int(time.time()))
    dst = (app.root_path + "/options_backups/options_{}.json".format(t))
    shutil.copyfile(src, dst)
    while len(glob.glob(app.root_path + "/options_backups/*.json")) > 5:
        old_bus = glob.glob(app.root_path + "/options_backups/*.json").sort()
        print("Deleting {} now!".format(old_bus[0]))
        os.remove(old_bus[0])


@app.route('/')
def gen_show():
    loadOptions()
    title = pick("title")
    char1 = pick("char1")
    para = pick("para")
    desc = fillBlanks(para, char1)
    return render_template("index.html", title=title.upper(), desc=sentenceCapitaliser(desc))


@app.route('/edit', methods=["GET", "POST"])
def edit():
    loadOptions()
    opts = dictToString(options)
    EditForm = forms.EditForm(
        f_title=opts["title"],
        f_place=opts["place"],
        f_char1=opts["char1"],
        f_char2=opts["char2"],
        f_char2_possession=opts["char2_possession"],
        f_relationship=opts["relationship"],
        f_shared_interest=opts["shared_interest"],
        f_mission=opts["mission"],
        f_firstname=opts["firstname"],
        f_surname=opts["surname"],
        f_historic_element=opts["historic_element"],
        f_historic_where=opts["historic_where"],
        f_action=opts["action"],
        f_para=opts["para"],
        f_final=opts["final"]
    )
    if request.method == "GET":
        return render_template("edit.html", EditForm=EditForm)
    if request.method == "POST":
        if EditForm.f_submit.data:
            print("Saving...")
            form_data = request.form
            m_data = marshalFormData(form_data)
            backupOptions()
            with open("options.json", mode="w") as outfile:
                json.dump(m_data, outfile)
            return redirect(url_for('gen_show'))


if __name__ == "__main__":
    app.run()
