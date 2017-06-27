import requests, lxml.html
from bs4 import BeautifulSoup
from flask import Flask

class Student:
    def __init__(self, name, status, score):
        self.name = name
        self.status = status
        self.score = score


def get_hidden_fields(response):
    login_html = lxml.html.fromstring(login.text)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')


s = requests.session()

home = 'http://187.19.195.156/Corpore.Net/Main.aspx?SelectedMenuIDKey=MainEducacional'
contexto = 'http://187.19.195.156/Corpore.Net/Source/Edu-Educacional/RM.EDU.CONTEXTO/EduSelecionarContextoModalWebForm.aspx?Qs=SelectedMenuIDKey%3dMainEducacional'

login = s.get('http://187.19.195.156/corpore.net/Login.aspx')
login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

form["txtUser"] = "201519019"
form["txtPass"] = "System.out"
form["ddlAlias"] = "CorporeRM"
form["btnLogin"] = "Acessar"

response = s.post('http://187.19.195.156/corpore.net/Login.aspx', data=form)

#print('senha utilizados' in response.text)

response = s.get("http://187.19.195.156/Corpore.Net/Source/Edu-Educacional/RM.EDU.CONTEXTO/EduSelecionarContextoModalWebForm.aspx?Qs=ActionID%3dEduNotaEtapaActionWeb%26SelectedMenuIDKey%3dmnNotasEtapa")


soup = BeautifulSoup(response.text, "lxml")
inputs = soup.find_all(id="rdContexto")
#print(inputs[1]["value"])
rdContexto = inputs[1]["value"]



#print(rdContexto)

page_html = lxml.html.fromstring(response.text)
hidden_inputs = page_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

form["rdContexto"] = rdContexto
response = s.post(contexto, data=form)


response = s.get("http://187.19.195.156/Corpore.Net/Main.aspx?ActionID=EduNotaEtapaActionWeb&SelectedMenuIDKey=mnNotasEtapa")

soup = BeautifulSoup(response.text, "lxml")
table = soup.find("table", {"id":"ctl24_xgvNotasFilial_DXMainTable"})

rows = table.findChildren(['th', 'tr'])

name = []
status = []
score = []
discipline = []

for row in rows[12:]:

    name = row.findChildren('td')[3].text
    status = row.findChildren('td')[4].text
    score = row.findChildren('td')[5].text, row.findChildren('td')[6].text, row.findChildren('td')[7].text,\
            row.findChildren('td')[8].text, row.findChildren('td')[9].text
    discipline.append(Student(name, status, score))


for student in discipline:
    print(student.name)
    print(student.status)
    print(student.score)
    print("\n")
























