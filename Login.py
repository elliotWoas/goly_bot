import requests
import spidermonkey
class login:
    host='http://erp.pgu.ac.ir'
    def __init__(self, userName, password):
        self.userName=userName
        self.password=password
    def getPayload(self, type, num):
        if  type.upper() == "TAB":
            return {'Command':'GET_TAB_INFO:'+num, 'userPosition':'undefined'}
        if  type.upper() == "ITEM":
            return {'Command':'ITEM_CLICK:'+num, 'userPosition':'undefined'}
    
    def encryptUserPassword(self):
        rt=spidermonkey.Runtime()
        cx=rt.new_context()
        jsfile=open('jscript.js', 'r');
        js=jsfile.read()
        cx.add_global('usern',self.userName)
        cx.add_global('passw',self.password)
        raw_results=cx.execute(js)
        results=list(raw_results)
        self.userName_encrypted =results[0]
        self.password_encrypted=results[1]
        self.login=results[2]
        del raw_results, results, js , jsfile
        
    def logIn(self):
        srequest=requests.Session()
        url = 'http://erp.pgu.ac.ir/SubSystem/Edari/PRelate/Site/Login.aspx?iftc=1'
        r1_get = srequest.get(url)        
        #the second post request
        payload={'Command':'LOGIN', 'username':self.userName_encrypted , 'password':self.password_encrypted,'username_txt':'', 'password_txt':''}
        r2_post=srequest.post(url,data=payload, cookies=r1_get.cookies)
        next_headers=r2_post.request.headers
        #adding Extra elements to headers
        next_headers['Referer']=r2_post.url
        next_headers['X-Requested-With']='XMLHttpRequest'
        next_headers['Host']='erp.pgu.ac.ir'
        url=r2_post.url
        r3_post=srequest.post(url,data=self.getPayload('tab', '020205'), headers=next_headers, cookies=r1_get.cookies)
        url=login.host+r3_post.content
        r4_get=srequest.get(url)
        self.html=r4_get.text.encode('UTF-8')
    @property
    def html(self):
        return self.html

