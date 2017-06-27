from bs4 import BeautifulSoup
import requests
import sys
import lxml

URL = 'http://187.19.195.156/corpore.net/Login.aspx'

def main():
    session = requests.Session()

    data_login = {
        '_EVENTTARGET': '',
        '_EVENTARGUMENT': '',
        '_VIEWSTATE': '/wEPDwULLTE1ODM3MjM0MjYPZBYCAgUPZBYCAgMPZBYKAgQPFgIeDUVudGVyRGlzYWJsZWQFBUZhbHNlZAIIDxYCHwAFBUZhbHNlZAIMDxBkDxYBZhYBEAUJQ29ycG9yZVJNBQlDb3Jwb3JlUk1nZGQCEA8PZBYCHg9EaXNhYmxlT25TdWJtaXQFBWZhbHNlZAISDw8WBB4LVXNlckNhcHRpb24FCFVzdcOhcmlvHhNDb25maXJtYXRpb25DYXB0aW9uBQVFbWFpbBYCHgdvbmNsaWNrBRFGb3Jnb3RQYXNzd29yZCgpO2RkBP+dXDZnsXeNB7Zi0nWMnQOkfLx1pb2Yxe5LNVmMusE=',
        '_VIEWSTATEGENERATOR': '67BA4204',
        '_EVENTVALIDATION': '/wEdAAXRucUfiyHY8AZFnilA2UGpDFTzKcXJqLg+OeJ6QAEa2kPTPkdPWl+8YN2NtDCtxie46B0WtOk572tmQWZGjlgiop4oRunf14dz2Zt2+QKDEBxncWFPbdn+2meH/pcIHYLAA5BjWMUUOu8xfqhKXRPe',
        'txtUser': '201519019',
        'txtPass': 'System.out123',
        'ddlAlias': 'CorporeRM',
        'btnLogin': 'Acessar'
    }

    r = session.post(URL, data=data_login)

    #r = session.get('http://187.19.195.156/Corpore.Net/Main.aspx?SelectedMenuIDKey=&ShowMode=2')


    soup = BeautifulSoup(r.text, "lxml")

    print(soup.prettify())
    print(r.headers)


main()

