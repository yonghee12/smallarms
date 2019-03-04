import sys
import pandas as pd
import numpy as np
import codecs

from datetime import timedelta
from datetime import datetime
from datetime import date

import urllib

day = '190220'
today = datetime.strptime(day, "%y%m%d").date()
yesterday = today - timedelta(days=1)

def hyphen_to_zero(hyphen_like):
    return int(str(hyphen_like).replace('-', '0').replace('.0', ''))

def hyphen_to_floatzero(hyphen_like):
    return float(str(hyphen_like).replace('-', '0'))

# filepath = path + 'report.xlsx'
filepath = '/Users/yonghee/Desktop/[QP] 현대카드_Reward광고 Daily Report_190220.xlsx'
rw = pd.read_excel(filepath, sheet_name = '매체별효율_{}월'.format(today.month), header = 3)
rw = rw.iloc[:, 1:4]
rw = rw.set_index('플랫폼')

df = rw

gubun = ''
num = 1
body = """{y}년 {m}월 {d}일 인스타그램, 유튜브 리워드광고 Daily Report 전달드립니다.
리포트는 전일({ym}월 {yd}일)까지 수치 기입하였습니다. 참고 부탁드립니다.

""".format(
y = today.year,
m = today.month,
d = today.day,
ym = yesterday.month,
yd = yesterday.day,
)

media = df.columns
for idx, medium in enumerate(media):
    element = """{num}. {medium} - {product}

<지표 성과>
· 집행 기간 : {aa}
· 일일 전환수 : {bb:,}
· 일일 실전환수 : {cc:,}
· 당일 잔존율 : {dd:.2%}
· {m}월 잔존율 : {ee:.2%}
· {m}월 목표 달성율 : {ff:.2%}

<운영 코멘트>

""".format(
        num = num,
        medium = medium,
        m = today.month,
        product = df.loc['매체명/상품', medium],
        aa = df.loc['(집행 기간)', medium],
        bb = df.loc['일일 리워드 전환수', medium],
        cc = df.loc['일일 실제 전환수', medium],
        dd = df.iloc[11, idx],
        ee = df.loc['기간 총 잔존율', medium],
        ff = df.loc['목표 달성률({}월)'.format(today.month), medium],
        )
    body += element
    num += 1
print(body)