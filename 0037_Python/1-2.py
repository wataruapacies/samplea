from selenium import webdriver
from time import sleep
import csv
import re
import pandas
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

def divide_addess(address):
    matches = re.match(r'(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|\
        那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|\
        廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|\
        .+?市.+?区|.+?[市区町村])(.+)' , address)
    return matches[1],matches[2],matches[3]

options = webdriver.ChromeOptions()

# user-agent
user_agent = ['e-mail:cgud4001@mail4.doshisha.ac.jp; Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',\
    'e-mail:cgud4001@mail4.doshisha.ac.jp; Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',\
    'e-mail:cgud4001@mail4.doshisha.ac.jp; Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',\
    'e-mail:cgud4001@mail4.doshisha.ac.jp; Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.3112.113 Safari/537.36'\
    ] 
options.add_argument('--user-agent=' + user_agent[random.randrange(0, len(user_agent), 1)])

driver = webdriver.Chrome('C:\\Users\\redst\\chromedriver',chrome_options=options) #第二引数の ,options=options はヘッドレスモードのするときのためだけに書き加えた

driver.get('https://www.gnavi.co.jp/')#いけたぞ

search_bar = driver.find_element_by_id("js-suggest-shop")
box_search="はまぐり"
search_bar.send_keys(box_search)

element = driver.find_element_by_class_name("p-search__submit")
element.click() #いけた！！
sleep(5)

csv_file_name = '1-2' + '.csv'

cols = ['店舗名', '電話番号','メールアドレス','都道府県','市区町村','番地','番地','URL','SSL']
df = pandas.DataFrame(index=[], columns=cols)

new=[]
name=[]
data_num=50

while True:
    links=[]
    new_name=[]
    c = driver.find_elements_by_css_selector(".style_titleLink__oiHVJ")
    for new_name in driver.find_elements_by_class_name("style_restaurantNameWrap__wvXSR"):
        name.append(new_name.text)
    links = [g.get_attribute('href') for g in c]
    new=new+links
    element = driver.find_element_by_class_name('style_nextIcon__M_Me_')
    if len(new)>data_num:
        break
    element.click()
    sleep(8)
dell = len(new)-data_num
del new[-dell:]
del name[-dell:]
print(name)
print(len(new))
for i in range(len(new)):
    driver.get(new[i])
    sleep(5)
    row=[]
    row.append(name[i])
    tel = driver.find_element_by_class_name("number")
    denwa=tel.text
    row.append(denwa)
    try:
        mail=driver.find_element(By.LINK_TEXT,"お店に直接メールする")
        mail_a=mail.get_attribute('a href')
        row,append(mail_a)
    except:
        row.append("")
    place = driver.find_element_by_class_name("region")
    address=place.text
    if __name__ == '__main__':
        address_v=divide_addess(address)
    row.append(address_v[0])
    row.append(address_v[1])
    row.append(address_v[2])
        
    try:
        building = driver.find_element_by_class_name("locality")
        row.append(building.text)
    except:
        row.append('')
    url_tmp = driver.find_element_by_css_selector(".sv-of.double")
    url=url_tmp.get_attribute('href')
    driver.get(url)
    sleep(7)
    url=driver.current_url
    row.append(url)
    if url.startswith('https'):
        row.append('TRUE')
    else:
        row.append('FALSE')
    print(row)
    del url
    df = df.append(pandas.Series(row, index=df.columns), ignore_index=True)
print(df)
df.to_csv(csv_file_name,index=False,encoding="shift_jis",errors='ignore')
print('finish')
driver.close()






