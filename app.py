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


# Cookie: _ga=GA1.2.406708436.1498888342; _gid=GA1.2.184563253.1498888342; _icl_visitor_lang_js=en-us; _mkto_trk=id:398-IBA-570&token:_mch-voxy.com-1498888349177-98776; my_language=en; sessionid=3rsoz2jf3i3n47egzbbv2fypyziwt3f8; SnapABugRef=https%3A%2F%2Fapp.voxy.com%2Fgo%2Flogin%20https%3A%2F%2Fvoxy.com%2F; SnapABugHistory=1#; SnapABugVisit=1#1498888355; SnapABugChatWindow=%7C0%7C-1%2C0%2C-1%2C0; __utma=173626660.406708436.1498888342.1498888356.1498888356.1; __utmb=173626660.1.10.1498888356; __utmc=173626660; __utmz=173626660.1498888356.1.1.utmcsr=voxy.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1

s = requests.session()
#s.cookies()


def get_hidden_fields(response):
    page_html = lxml.html.fromstring(response.text)
    hidden_inputs = page_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    return form


def do_all_stuff(username, password):
    LOGIN_URL = 'http://187.19.195.156/corpore.net/Login.aspx'
    CONTEXT_URL = 'http://187.19.195.156/Corpore.Net/Source/Edu-Educacional/RM.EDU.CONTEXTO/EduSelecionarContextoModalWebForm.aspx?Qs=SelectedMenuIDKey%3dMainEducacional'
    SCORE_URL = 'http://187.19.195.156/Corpore.Net/Source/Edu-Educacional/RM.EDU.CONTEXTO/EduSelecionarContextoModalWebForm.aspx?Qs=ActionID%3dEduNotaEtapaActionWeb%26SelectedMenuIDKey%3dmnNotasEtapa'

    disciplines = []

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
    if len(inputs) == 3:
        rdContexto = inputs[2]["value"]
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

    return disciplines


app = Flask(__name__.split('.')[0])



@app.route("/")
def main():
    return render_template("home.html")


@app.route("/getscore", methods=["POST"])
def get_score():
    username = request.form.get("username")
    password = request.form.get("password")

    # username = "201519019"
    # password = "System.out"

    # return render_template("score.html", disciplines=do_all_stuff(username, password))
    disciplines = do_all_stuff(username, password)
    return jsonify([dis.serialize() for dis in disciplines])


if __name__ == '__main__':
    app.run(debug=True)
