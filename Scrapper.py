from bs4 import BeautifulSoup as BS
class scrapper:
    def __init__(self, rc):
        self.raw_content=rc
    def getSemesterName(self, table, semester):
        prev_sibl=table.previous_sibling.previous_sibling
        semester['name']=prev_sibl.string 
        
    def getSemesterGrades(self, table, semester):
        trs=table.find_all('tr', recursive=False)
        j=0
        lessons=[]
        for tr in trs:
            if j <>  0:
                tds=tr.find_all('td', recursive=False)
                i=0
                lesson={}
                for td in tds:
                    if i==1:
                        lesson['name']=td.span.string
                    elif i==6:
                        lesson['grade']=td.span.string
                    elif i==7:
                        lesson['score']=td.span.string
                    i+=1
                lessons.append(lesson)    
            j+=1
        semester['lessons']=lessons        

    def  make(self):    
        bs=BS(self.raw_content, 'lxml')
        div_gridSecond=bs.find(id='gridSecond')
        tables_grd=div_gridSecond.find_all('table', class_='grd', recursive=False)
        self.semesters=[]
        for table in tables_grd:
            semester={}
            self.getSemesterName(table, semester)
            self.getSemesterGrades(table, semester)
            self.semesters.append(semester)
        
    @property    
    def text(self):
        text=""
        for s in self.semesters:
            text=text+s['name']
            for lesson in s['lessons']:
                text=text+lesson['name']+' : '+str(lesson['grade'])+" : "+str(lesson['score'])+'\n'
        return text  
if __name__=='__main__':
    ss=scrapper(open('res.html', 'r').read())
    ss.make()
    
