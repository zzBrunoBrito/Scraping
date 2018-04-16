import requests, lxml.html
from bs4 import BeautifulSoup
from markupsafe import Markup
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify


class Discipline:
    def __init__(self, name, status, score):
        self.name = name
        self.status = status
        self.score = score

    def serialize(self):
        return {
            'name': self.name,
            'status': self.status,
            'score': self.score
        }


class Url:
    LOGIN_URL = 'http://187.19.195.156/corpore.net/Login.aspx'
    CONTEXT_URL = 'http://187.19.195.156/Corpore.Net/Source/Edu-Educacional/RM.EDU.CONTEXTO/EduSelecionarContextoModalWebForm.aspx?Qs=SelectedMenuIDKey%3dMainEducacional'
    SCORE_URL = 'http://187.19.195.156/Corpore.Net/Source/Edu-Educacional/RM.EDU.CONTEXTO/EduSelecionarContextoModalWebForm.aspx?Qs=ActionID%3dEduNotaEtapaActionWeb%26SelectedMenuIDKey%3dmnNotasEtapa'
    FAULT_URL = 'http://187.19.195.156/Corpore.Net/Main.aspx?ActionID=EduQuadroAvisoActionWeb&SelectedMenuIDKey=mnQuadroAviso'
    SCORE = 'http://187.19.195.156/Corpore.Net/Main.aspx?ActionID=EduNotaEtapaActionWeb&SelectedMenuIDKey=mnNotasEtapa'


def get_hidden_fields(response):
    page_html = lxml.html.fromstring(response.text)
    hidden_inputs = page_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    return form


def login(username, password):
    session = requests.session()

    login = session.get(Url.LOGIN_URL)

    form = get_hidden_fields(login)

    form["txtUser"] = str(username)
    form["txtPass"] = str(password)
    form["ddlAlias"] = "CorporeRM"
    form["btnLogin"] = "Acessar"

    session.post(Url.LOGIN_URL, data=form)

    response = session.get(Url.SCORE_URL)

    return session, response


def get_page(response, session, url, context_number=-1):
    soup = BeautifulSoup(response.text, "lxml")
    inputs = soup.find_all(id="rdContexto")

    rd_context = inputs[context_number]['value']

    if rd_context:
        form = get_hidden_fields(response)
        form["rdContexto"] = rd_context

        session.post(Url.CONTEXT_URL, data=form)

        response = session.get(url)
        return session, response


class Context:
    def __init__(self, session, response):
        self.session = session
        self.response = response


def get_disciplines(response):
    disciplines = []

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"id": "ctl24_xgvNotasFilial_DXMainTable"})

    rows = table.findChildren(['th', 'tr'])

    for row in rows[12:]:
        name = row.findChildren('td')[3].text
        status = row.findChildren('td')[4].text
        score = row.findChildren('td')[5].text, row.findChildren('td')[6].text, row.findChildren('td')[7].text, \
                row.findChildren('td')[8].text, row.findChildren('td')[9].text
        yield Discipline(name, status, score)

    return disciplines


app = Flask(__name__.split('.')[0])


@app.route("/")
def main():
    return render_template("home.html")


@app.route("/getscore", methods=["POST"])
def get_score():

    username = request.form.get("username")
    password = request.form.get("password")

    session, response = login(username, password)
    session, response = get_page(response, session, Url.SCORE)

    return render_template("score.html", disciplines=get_disciplines(response))
    # disciplines = do_all_stuff(username, password)
    # return jsonify([dis.serialize() for dis in disciplines])


if __name__ == '__main__':
    app.run(debug=True)
