import Login
import Scrapper
from sys import argv
userName = str(argv[1])
passWord = str(argv[2])
login=Login.login(userName, passWord)
login.encryptUserPassword()
login.logIn()
html=login.html
scpr=Scrapper.scrapper(html)
scpr.make()
file=open('res.text', 'w')
file.write(scpr.text.encode('UTF-8'))
file.close()
