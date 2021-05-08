from bs4 import BeautifulSoup
import requests
import re, json
from function import nepali_word_filter,word_filter,int_pair,word_indent,word2vec

# web scrapping code
class Web_scrape:
    
    def __init__(self,url=None):
        self.url = url
        self.hospital = []
        self.cities=[]
        self.banks = []
        self.nep_text=[]
        self.glob_arr=[]
        self.news_href=['https://crimenewsnepal.com/category/robbery','https://crimenewsnepal.com/category/apf','https://crimenewsnepal.com/category/crime-news','https://crimenewsnepal.com/category/acc']

    
    def html_render(self):
        source=requests.get(self.url).text
        soup= BeautifulSoup(source,"html.parser")
        return soup
    
    def text_finder(self,link):
        self.url = link
        load_html = self.html_render()
        parent= load_html.find('div',class_='newsDetailContentWrapper')
    
        for i in parent.find_all('p'):
            new_text = nr.romanize_text(i.text)
            print(new_text,'end')
            filt_text=new_text.replace("\n", " ")
            filt_text=filt_text.strip()
            self.glob_arr.append(filt_text)
    
    def array_to_json(filename,array):
        with open(f'{filename}.json','w',encoding='utf-8') as outfile:
            json.dump(array,outfile,ensure_ascii=False)
        output = f'{filename} has been saved as json file' 
        return output
    
    def json_to_array(filename):
        with open(f'{filename}.json',encoding="utf8") as json_file:
            jsonarr = json.load(json_file)
            return jsonarr
    

    def nep_to_roman(array):
        rom_text = []

        for i in array:
            new_txt = nepali_word_filter(i)
            new_txt=nr.romanize_text(new_txt)
            rom_text.append(new_txt)

        return rom_text



    
    def comm_check(self,string):

        hospital_common=['अस्पताल','केन्द्र','गृह','औषधालय','आयुर्वेद','स्वास्थ्यकेन्द्र']
        words = string.split(" ")
        for w in words:
            if w in hospital_common:
                if words[-1] in self.cities:
                    
                    new_text= string.rsplit(' ', 1)[0]
                    self.hospital.append(new_text)
                    
                else:               
                    self.hospital.append(string)
                break
    
    def city_scraper(self):
        
        load_html = self.html_render()
        parent= load_html.find_all('table',class_='wikitable sortable')
    
        for j in range(len(parent)):
            child = parent[j].find_all('tr')
            for i in range(len(child)):
                if i != 0:
                    all_td = child[i].find_all('td')[2].text
                    new_txt = re.sub(r'\n','',all_td)
                    if new_txt not in self.cities:
                        
                        self.cities.append(new_txt)
                        
        romanize_arr = self.nep_to_roman(self.cities)
        #saving arrays as json file for future use
        self.array_to_json('cities',romanize_arr)
        
    
    def hospital_finder(self):

        load_html = self.html_render()
        parent = load_html.find('div',{'class':'mw-parser-output'})
        child = parent.find_all('p')
        for i in child:
            poss = i.find_all('a')

            if poss == None:
                self.comm_check(i.text)
                         
            else:
                if len(poss) == 1:
                    
                    self.comm_check(poss[0].text)
                elif len(poss) > 1:
                    
                    for j in poss:
                            if ',' in j.text:
                                old_text = j.text.split(",")
                                new_text = old_text[0]
                                self.comm_check(new_text)
                            else:
                                self.comm_check(j.text)
                                
        romanize_arr = self.nep_to_roman(self.hospital)
        #saving arrays as json file for future use
        self.array_to_json('hospital',romanize_arr)
    
    def bank_scrapper(self):
        load_html = self.html_render()
        parent = load_html.find('div',{'class':'mw-parser-output'})
        child = parent.find_all('a')
        for i in child:
            new_txt = i.text
            if 'लिमिटेड' in new_txt:
                new_txt = nr.romanize_text(i.text)
                self.all_banks.append(new_txt)

        romanize_arr = self.nep_to_roman(self.all_banks)
        #saving arrays as json file for future use
        self.array_to_json('banks',romanize_arr)
        

    def nepali_text_scrapper(self):
        for j in range(len(self.news_href)):
            self.url = self.news_href[j]
            load_html = self.html_render()
            page_n = load_html.find('div',class_='nav-links')
            nex = page_n.find('a',class_='next page-numbers')
            page_n = int(nex.find_previous('a').text)
            print(page_n)
            for i in range(page_n):

                new_source = None
                if i == 0:
                    self.url=requests.get(self.news_href[j]).text
                else:
                    self.url=requests.get(f'{self.news_href[j]}/page/{i+1}').text
                soup = self.html_render()
                regex = re.compile('.*post.*')
                post = soup.find_all("article",{"class":regex})
                for div in post:
                    link=str(div.a['href'])
                    self.text_finder(link)

        romanize_arr = self.nep_to_roman(self.glob_arr)
        #saving arrays as json file for future use
        self.array_to_json('news_article',romanize_arr)
        
    



                

    


web = Web_scrape('https://ne.wikipedia.org/wiki/नेपालका_अस्पतालहरू')
print(web.hospital_finder())
