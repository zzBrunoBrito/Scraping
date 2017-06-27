import requests, lxml.html
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template
from flask import request

class Discipline:
    def __init__(self, name, status, score):
        self.name = name
        self.status = status
        self.score = score

disciplines = []

def get_hidden_fields(response):
    page_html = lxml.html.fromstring(response.text)
    hidden_inputs = page_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    return form

def do_all_stuff(username, password):
    LOGIN_URL = 'http://187.19.195.156/corpore.net/Login.aspx'
    CONTEXT_URL = 'http://187.19.195.156/Corpore.Net/Source/Edu-Educacional/RM.EDU.CONTEXTO/EduSelecionarContextoModalWebForm.aspx?Qs=SelectedMenuIDKey%3dMainEducacional'
    SCORE_URL = 'http://187.19.195.156/Corpore.Net/Source/Edu-Educacional/RM.EDU.CONTEXTO/EduSelecionarContextoModalWebForm.aspx?Qs=ActionID%3dEduNotaEtapaActionWeb%26SelectedMenuIDKey%3dmnNotasEtapa'

    session = requests.session()

    login = session.get(LOGIN_URL)

    form = get_hidden_fields(login)

    form["txtUser"] = str(username)
    form["txtPass"] = str(password)
    form["ddlAlias"] = "CorporeRM"
    form["btnLogin"] = "Acessar"

    session.post(LOGIN_URL, data=form)

    response = session.get(SCORE_URL)

    soup = BeautifulSoup(response.text, "lxml")
    inputs = soup.find_all(id="rdContexto")
    if len(inputs) == 2:
        rdContexto = inputs[1]["value"]
    else:
        rdContexto = inputs[0]["value"]

    form = get_hidden_fields(response)
    form["rdContexto"] = rdContexto

    session.post(CONTEXT_URL, data=form)

    response = session.get(
        "http://187.19.195.156/Corpore.Net/Main.aspx?ActionID=EduNotaEtapaActionWeb&SelectedMenuIDKey=mnNotasEtapa")

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"id": "ctl24_xgvNotasFilial_DXMainTable"})
    rows = table.findChildren(['th', 'tr'])

    name = []
    status = []
    score = []


    for row in rows[12:]:
        name = row.findChildren('td')[3].text
        status = row.findChildren('td')[4].text
        score = row.findChildren('td')[5].text, row.findChildren('td')[6].text, row.findChildren('td')[7].text, \
                row.findChildren('td')[8].text, row.findChildren('td')[9].text
        disciplines.append(Discipline(name, status, score))



app = Flask(__name__.split('.')[0])

@app.route("/")
def main():
    return render_template("home.html")

@app.route("/getscore", methods=["POST"])
def get_score():
    username = request.form.get("username")
    password = request.form.get("password")

    print(username)
    print(password)

    #username = "201519019"
    #password = "System.out"
    do_all_stuff(username, password)
    return render_template("score.html", disciplines=disciplines)

#app.run()
