from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException, StaleElementReferenceException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import sys
import time
import numpy as np
import pandas as pd
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
import urllib

class insta():

    def chrome_open(self):
    
        options = webdriver.ChromeOptions()
#         options.add_argument('headless')
        options.add_argument('window-size=640*480')
        options.add_argument('no-sandbox')
        options.add_argument('disable-dev-shm-usage')
        options.add_argument("disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
        options.add_argument("lang=ko_KR")
        options.add_argument("disable-infobars")    
        #options.add_argument("start.maximized")
        self.driver = webdriver.Chrome('/Users/yonghee/chromedriver', options=options)
        self.driver.get('about:blank')

        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
        self.driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
        self.driver.implicitly_wait(10)

p = insta()
p.chrome_open()
keywords = [
    '현대카드', '삼성카드', '신한카드', '롯데카드', '국민카드',
    '쿠킹라이브러리', '뮤직라이브러리', '트래블라이브러리', '디자인라이브러리',
    '현대모터스튜디오', '비트360', 'my클럽고메', 
]

keywords = [
    '현대카드뉴레트로', '2019현대카드컬처테마', '뉴레트로', '아주오래된미래', '현대카드', 
    'HyundaiCard', '전국LP자랑', '현대카드디자인라이브러리', '디자인라이브러리', 'DesignLibrary', 
    '현대카드DesignLibrary', '현대카드트래블라이브러리', '트래블라이브러리', 'TravelLibrary', 
    '현대카드TravelLibrary', '현대카드뮤직라이브러리', '뮤직라이브러리', 'MusicLibrary', 
    '현대카드MusicLibrary', '현대카드쿠킹라이브러리', '쿠킹라이브러리', 'CookingLibrary', 
    '현대카드CookingLibrary', '언더스테이지', 'Understage', '현대카드언더스테이지', 
    '현대카드understage', '바이닐앤플라스틱', '현대카드바이닐앤플라스틱', 'VinylAndPlastic', 
    '현대카드VinylandPlastic']

df = pd.DataFrame()
direct = {'tags' : [], 'numbers' : []}

for keyword in keywords[:2]:
    keyword_t = urllib.parse.urlencode({'':keyword})[1:]
    p.driver.get('https://www.instagram.com/explore/tags/{}/?hl=ko'.format(keyword_t))
    

    p.driver.implicitly_wait(3)
    # time.sleep(4)
    p.driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(keyword)

    p.driver.implicitly_wait(3)
    time.sleep(5)

    page = p.driver.page_source
    bs = BeautifulSoup(page, "lxml")
    fuq = bs.find('div', {'class' : 'fuqBx'})
    if fuq == None:
        time.sleep(5)
        fuq = bs.find('div', {'class' : 'fuqBx'})
    yce = fuq.findAll('a', {'class' : 'yCE8d'})
    
    tag_name_list, n_posts_list = [], []
    for y in yce[:]:
        if y['href'][:14] == '/explore/tags/':
            tag_name = y.div.div.find('span', {'class' : 'Ap253'}).text[1:]
            n_posts = y.div.div.find('div', {'class' : "Fy4o8"}).text[4:]
            tag_name_list.append(tag_name)
            n_posts_list.append(n_posts)
            print(tag_name, n_posts)
    n_posts_list = list(map(lambda x: int(x.replace(',', '')), n_posts_list))
    dic = {'tags' : tag_name_list, 'numbers' : n_posts_list}
    df = df.append(pd.DataFrame(dic))
    
    # Direct Numbers
    number = bs.find('span', {'class' : 'g47SY '})
    if not number:
        number = bs.find('span', {'class' : 'g47SY'})
    number = number.text
    direct['tags'].append(keyword)
    direct['numbers'].append(number)
#     df = pd.DataFrame(dic)

#     with pd.ExcelWriter('output.xlsx') as writer:
#         df1.to_excel(writer, sheet_name='Sheet_name_1')
#         df2.to_excel(writer, sheet_name='Sheet_name_2')
    time.sleep(2)
df2 = pd.DataFrame(direct)
df2.to_excel('hastags_direct.xlsx')
df.to_excel('hastags.xlsx')

# p.driver.implicitly_wait(3)