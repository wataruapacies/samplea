import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import csv
import datetime
import urllib.parse
from time import sleep
import urllib.request
import lxml.html
import pandas

def divide_addess(address):
    matches = re.match(r'(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|\
        那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|\
        廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|\
        .+?市.+?区|.+?[市区町村])(.+)' , address)
    return matches[1],matches[2],matches[3]

data_num=50
today = datetime.datetime.today().strftime("%Y%m%d")

search = "お好み焼き"
search_magic = urllib.parse.quote(search)
 
ua=UserAgent()
headers = {'usar-agent':ua.chrome}

url = 'https://r.gnavi.co.jp/area/jp/'
page_num=1
restaurant_names=[]
restaurant_links=[]
while page_num<4:
    next_url = url + 'rs/?date=' + today + '&fw=' + search_magic + '&p=' + str(page_num)
    page_num += 1
    sleep(3)
    res = requests.get(next_url,headers=headers,timeout=15)
    res_soup = BeautifulSoup(res.text,"html.parser")
    elems = res_soup.find_all("h2",class_="style_restaurantNameWrap__wvXSR")
    names=[elem.get_text() for elem in elems]
    restaurant_names=restaurant_names+names
    elems_url = res_soup.find_all("a",class_="style_titleLink__oiHVJ")
    links = [elem_url.attrs['href'] for elem_url in elems_url]
    restaurant_links=restaurant_links+(links)
    if len(restaurant_names)>data_num:
        break

dell = len(restaurant_names) - data_num
del restaurant_names[-dell:]
del restaurant_links[-dell:]
print(restaurant_names)



cols = ['店舗名', '電話番号','メールアドレス','都道府県','市区町村','番地','建物名','URL','SSL']
df = pandas.DataFrame(index=[], columns=cols)

csv_file_name = 'lets_try' + '.csv'

for i in range(len(restaurant_names)):
    sleep(3)
    response = requests.get(restaurant_links[i],headers=headers,timeout=15)
    row=[]
    row.append(restaurant_names[i])
    #print(restaurant_names[i])
    response_soup = BeautifulSoup(response.text,"html.parser")
    tel = response_soup.find("span",class_="number")
    denwa=tel.get_text()
    row.append(denwa)
    #print(denwa)
    url_mail=restaurant_links[i]
    res_mail=urllib.request.urlopen(url_mail)
    dom=lxml.html.fromstring(res_mail.read())
    try:
        s=dom.xpath('string(//tbody/tr/td/ul/li/a[contains(text(),"メール")])')
        mail_a=s.attrs["href"]
        row.append(mail_a)
    except:
        row.append("")
    
    r = BeautifulSoup(response.content,"html.parser")
    place = r.find("span",class_="region")
    #print(place)
    address=place.get_text()
    address_v=[]
    #print(address)
    address_v=divide_addess(address)
    row.append(address_v[0])
    row.append(address_v[1])
    row.append(address_v[2])
    
    b = BeautifulSoup(response.content,"html.parser")
    
    try:
        building = b.find("span",class_="locality")
        row.append(building.get_text())
    except:
        row.append('')
    row.append('')
    row.append('')
    df = df.append(pandas.Series(row, index=df.columns), ignore_index=True)
    print(row)


print(df)
df.to_csv(csv_file_name,index=False,encoding="cp932",errors='ignore')
print('建物名な！！！！')

