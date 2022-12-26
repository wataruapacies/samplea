from urllib import request  # urllib.requestモジュールをインポート
from bs4 import BeautifulSoup  # BeautifulSoupクラスをインポート

url='https://www.jleague.jp/standings/j1/'
response = request.urlopen(url)
soup = BeautifulSoup(response,"html.parser")
response.close()

header = soup.find('tr')
#print(header)


table = soup.find_all('tr')
#print(table[1])

standing = []
for row in table:
    tmp = []
    for item in row.find_all('td'):
        if item.a:
            tmp.append(item.text[0:len(item.text) // 2])
        else:
            tmp.append(item.text)
    del tmp[0]
    del tmp[-1]
    standing.append(tmp)

for item in standing:
    print(item)
'''
「Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER.」と表示されているのは、
BeautifulSoupオブジェクトの生成時に内部でHTMLの解析がうまくいかなかったことを示す警告だ。ここでは無視してもよい
（以下のコラムも参照のこと）。
'''