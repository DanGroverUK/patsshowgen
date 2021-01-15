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
        options = json.load(fo)
    return options


def sentenceCapitaliser(para):
    sentences = para.split(". ")
    sentences2 = [sentence[0].capitalize() + sentence[1:]
                  for sentence in sentences]
    string2 = '. '.join(sentences2)
    return string2


def pick(filler):
    options = loadOptions()
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


def dictToForm(options):
    EditForm = forms.EditForm()
    for k in options.keys():
        newstr = ""
        fieldname = "f_" + k
        for o in options[k]:
            newstr = newstr + str(o) + "\n"
        EditForm[fieldname].data = newstr
        if k != "para":
            EditForm[fieldname].render_kw["rows"] = (len(options[k]) + 3)
        else:
            EditForm[fieldname].render_kw["rows"] = (len(options[k]) * 4)
    return EditForm


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
    for r, d, f in os.walk((app.root_path + "/options_backups/*.json")):
        if len(f) > 5:
            f.sort()
            os.remove(os.path.join(r, f[0]))


@app.route('/')
def gen_show():
    title = pick("title")
    char1 = pick("char1")
    para = pick("para")
    desc = fillBlanks(para, char1)
    return render_template("index.html", title=title.upper(), desc=sentenceCapitaliser(desc))


@app.route('/edit', methods=["GET", "POST"])
def edit():
    options = loadOptions()
    EditForm = dictToForm(options)
    if request.method == "GET":
        return render_template("edit.html", EditForm=EditForm)
    if request.method == "POST":
        if EditForm.f_submit.data:
            print("Saving...")
            form_data = request.form
            m_data = marshalFormData(form_data)
            backupOptions()
            options_f = (app.root_path + "/options.json")
            with open(options_f, mode="w") as outfile:
                json.dump(m_data, outfile)
            return redirect(url_for('gen_show'))


if __name__ == "__main__":
    app.run(debug=True)
