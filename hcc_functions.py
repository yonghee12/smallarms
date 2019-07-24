import sys
import pandas as pd
import numpy as np
import codecs

from datetime import date
from datetime import timedelta
from datetime import datetime

import urllib


def hyphen_to_zero(hyphen_like):
    if type(hyphen_like) == int:
        return hyphen_like
    elif type(hyphen_like) == float:
        return int(hyphen_like)
    hyphen_like = hyphen_like.replace('\n', '').replace("%", "")
    return int(str(hyphen_like).replace('-', '0').replace('.0', ''))

def hyphen_to_floatzero(hyphen_like):
    if type(hyphen_like) == float:
        return hyphen_like
    elif type(hyphen_like) == int:
        return float(hyphen_like)
    hyphen_like = hyphen_like.replace('\n', '').replace("%", "")
    return float(str(hyphen_like).replace('-', '0'))

def yt(day, path, week, today, yesterday):
    try:
        filepath = path + 'report.xlsx'
        yt = pd.read_excel(filepath, sheet_name = week, header = 3)
        print(type(yt), week)
        
        yt = yt.iloc[1:, :]
        yt.columns = [
            '구분', '날짜', '소재', '광고타겟', '예산(vat포함)', '예산', '소진금액', 
            '소진금액(vat포함)', '노출', '클릭', '조회', 'CTR', 'VTR', 'CPM',
            'CPC', 'CPV', '영상 재생률 25%', '영상 재생률 50%', '영상 재생률 75%', 
            '영상 재생률 100%', '영상 좋아요', '채널 구독', '링크'
        ]
        yt.iloc[:, :4] = yt.iloc[:, :4].fillna(method='ffill')
        yt.iloc[:, 4:] = yt.iloc[:, 4:].fillna(0)
        yt = yt.reset_index(drop=True)

    # YT PRINT
        df = yt
        print(df)
        gubun = ''
        num = 1
        body = '[유튜브]\n\n'

        for row in df.iloc[:, :].iterrows():
            data = row[1]
            if data['구분'] != '합계/평균':
                gubun = data['구분']
                continue
            elif data['구분'] == '합계/평균':
                element = """{}. {:} : {:}

    <지표 성과>
    · 달성 노출 : {:,} Imps
    · 달성 조회 : {:,} View
    · VTR : {:.2%}
    · CPM : {:,.0f}원
    · CPV : {:,.0f}원
    · 동영상 재생진행률
    &emsp;- 25% : {:.2%}
    &emsp;- 50% : {:.2%}
    &emsp;- 75% : {:.2%}
    &emsp;- 100% : {:.2%}

    · 관심사 타겟 정보 :

    <운영 코멘트>
    · 
    · VTR {:.2%}, CPV {:,.0f}원으로 .. 수치 보이며
    · 
    · 


    """.format(
                    num,
                    gubun.replace('\n', ' ').replace("  ", ' ').replace("  ", ' ').strip(),
                    data['날짜'].replace('\n', ' '),
                    hyphen_to_zero(data['노출']),
                    hyphen_to_zero(data['조회']),
                    hyphen_to_floatzero(data['VTR']),
                    hyphen_to_floatzero(data['CPM']),
                    hyphen_to_floatzero(data['CPV']),
                    hyphen_to_floatzero(data['영상 재생률 25%']),
                    hyphen_to_floatzero(data['영상 재생률 50%']),
                    hyphen_to_floatzero(data['영상 재생률 75%']), 
                    hyphen_to_floatzero(data['영상 재생률 100%']),
                    hyphen_to_floatzero(data['VTR']),
                    hyphen_to_floatzero(data['CPV']),
                )
        #         print(element)
                body += element
                num += 1
        body += """
        데일리리포트 관련하여 자세한 사항은 아래 첨부파일 확인 부탁드립니다.

        감사합니다.
        김희중 드림
        
        """

        # print(body)
        f = codecs.open(path + 'txt/' + '{}_{}_YT.txt'.format(day, week), 'w', encoding='cp949')
        f.write(body)
        f.close()
        print('{}_{}_YT.txt'.format(day, week), '생성 완료')

    except FileNotFoundError as e:
        print(e)
        print("해당 리포트가 없습니다.")
        return "잘못된 리포트입니다."

        # print(body)
        
    body = body.replace("\n", "<br>")
    return body


def ig(day, path, week, today, yesterday):
    try:
        filepath = path + 'report.xlsx'
        ig = pd.read_excel(filepath, sheet_name = week, header = 3)
        ig = ig.iloc[1:, :]
        ig.columns = [
            '구분', '날짜', '소재', '광고 타겟', '모수', '예산(vat포함)', '예산', '소진금액',
            '소진 금액(vat포함)', '광고도달', '노출', '클릭', '링크클릭', 
            'Video Views (3초+)', 'Video Views (100%)',
            'Reaction(Like)', 'Reaction(Share)', 'Reaction(Comment)', 'Reaction(Total)',
            'CTR', 'CPM', 'CPC', '링크클릭CPC', 'CPV', 
            'CPI(인터렉션)', '링크'
        ]
        ig.iloc[:, :4] = ig.iloc[:, :4].fillna(method='ffill')
        ig.iloc[:, 4:] = ig.iloc[:, 4:].fillna(0)
        ig = ig.reset_index(drop=True)

    # IG PRINT
        df = ig

        gubun = ''
        num = 1
        body = '[인스타그램]\n\n'
        for row in df.iloc[:, :].iterrows():
            data = row[1]
            if data['구분'] != '합계/평균':
                gubun = data['구분']
            elif data['구분'] == '합계/평균':
                if "트래픽" in gubun:
                    element = """{}. {:} : {:}

                    <지표 성과>
                    · 달성 노출 : {:,} Imps
                    · 달성 클릭 : {:,} Clicks
                    · 링크 클릭 : {:,} Clicks
                    · CTR : {:.2%}
                    · CPM : {:,.0f}원
                    · CPC : {:,.0f}원
                    · 링크 클릭 CPC : {:,.0f}원
                    · CPI : {:,.0f}원
                    · 컨텐츠 반응 : {:,} Like / {:,} Share / {:,} Comment

                    · 관심사 타겟 정보 :

                    <운영 코멘트>
                    · 
                    · CTR {:.2%}, CPC {:,.0f}원, CPI {:,.0f}원, CPM {:,.0f}원
                    · 
                    · 


        """.format(
                    num,
                    gubun.replace('\n', ' ').replace("  ", ' ').replace("  ", ' ').strip(),
                    data['날짜'].replace('\n', ' '),
                    hyphen_to_zero(data['노출']),
                    hyphen_to_zero(data['클릭']),
                    hyphen_to_zero(data['링크클릭']),
                    hyphen_to_floatzero(data['CTR']),
                    hyphen_to_floatzero(data['CPM']),
                    hyphen_to_floatzero(data['CPC']),
                    hyphen_to_floatzero(data['링크클릭CPC']),
                    hyphen_to_floatzero(data['CPI(인터렉션)']),
                    hyphen_to_zero(data['Reaction(Like)']),
                    hyphen_to_zero(data['Reaction(Share)']),
                    hyphen_to_zero(data['Reaction(Comment)']),
                    hyphen_to_floatzero(data['CTR']),
                    hyphen_to_floatzero(data['CPC']),
                    hyphen_to_floatzero(data['CPI(인터렉션)']),
                    hyphen_to_floatzero(data['CPM']),
                    )
                    body += element
                    num += 1

                else:
                    element = """{}. {:} : {:}

                    <지표 성과>
                    · 달성 노출 : {:,} Imps
                    · 달성 클릭 : {:,} Clicks
                    · CTR : {:.2%}
                    · CPM : {:,.0f}원
                    · CPC : {:,.0f}원
                    · CPI : {:,.0f}원
                    · 컨텐츠 반응 : {:,} Like / {:,} Share / {:,} Comment

                    · 관심사 타겟 정보 :

                    <운영 코멘트>
                    · 
                    · CTR {:.2%}, CPC {:,.0f}원, CPI {:,.0f}원, CPM {:,.0f}원
                    · 
                    · 


        """.format(
                    num,
                    gubun.replace('\n', ' ').replace("  ", ' ').replace("  ", ' ').strip(),
                    data['날짜'].replace('\n', ' '),
                    hyphen_to_zero(data['노출']),
                    hyphen_to_zero(data['클릭']),
                    hyphen_to_floatzero(data['CTR']),
                    hyphen_to_floatzero(data['CPM']),
                    hyphen_to_floatzero(data['CPC']),
                    hyphen_to_floatzero(data['CPI(인터렉션)']),
                    hyphen_to_zero(data['Reaction(Like)']),
                    hyphen_to_zero(data['Reaction(Share)']),
                    hyphen_to_zero(data['Reaction(Comment)']),
                    hyphen_to_floatzero(data['CTR']),
                    hyphen_to_floatzero(data['CPC']),
                    hyphen_to_floatzero(data['CPI(인터렉션)']),
                    hyphen_to_floatzero(data['CPM']),
                    )
                    body += element
                    num += 1


        # print(body)
        f = codecs.open(path +  'txt/' + '{}_{}_IG.txt'.format(day, week), 'w', encoding='cp949')
        f.write(body)
        f.close()
        print('{}_{}_IG.txt'.format(day, week), '생성 완료')
    except FileNotFoundError as e:
        print(e)
        print("Instagram 리포트가 없습니다.")
    body = body.replace("\n", "<br>")
    return body


def fb(day, path, week, today, yesterday):
    try:
        filepath = path + 'report.xlsx'
        fb = pd.read_excel(filepath, sheet_name = week, header = 3)
        fb = fb.iloc[1:, :]
        fb.columns = [
            '구분', '날짜', '소재', '광고 타겟', '모수', '예산(vat포함)', '예산', '소진금액',
            '소진 금액(vat포함)', '광고도달', '노출', '클릭', 'CPL', '링크클릭', 
            'Video Views (3초+)', 'Video Views (100%)',
            'Reaction(Like)', 'Reaction(PageLike)','Reaction(Share)', 
            'Reaction(Comment)', 'Reaction(Total)',
            'CTR', 'CPM', 'CPC', '링크클릭CPC', 'CPV', 
            'CPI(인터렉션)', '링크'
        ]
        fb.iloc[:, :4] = fb.iloc[:, :4].fillna(method='ffill')
        fb.iloc[:, 4:] = fb.iloc[:, 4:].fillna(0)
        fb = fb.reset_index(drop=True)

    # FB PRINT
        df = fb

        gubun = ''
        num = 1
        # body = ''
        body = """안녕하세요,
        퀀텀파이러츠 김희중입니다.
        
        {y}년 {m}월 {d}일 페이스북, 인스타그램, 유튜브 콘텐츠광고 Daily Report 전달해드립니다.
리포트는 전일({ym}월 {yd}일)까지 수치 기입하였습니다. 참고 부탁드립니다.

---  

<금일 이슈>

금일 안내드리는 종료 예정 캠페인입니다.
·  : FB, IG, YT
·  : FB, IG, YT

---

[페이스북]  

""".format(
y = today.year,
m = today.month,
d = today.day,
ym = yesterday.month,
yd = yesterday.day,
)
        for row in df.iloc[:, :].iterrows():
            data = row[1]
            if data['구분'] != '합계/평균':
                gubun = data['구분']
            elif data['구분'] == '합계/평균':
                if "트래픽" in gubun:
                    element = """{}. {:} : {:}

        <지표 성과>
        · 달성 노출 : {:,.0f} Imps
        · 달성 클릭 : {:,.0f} Clicks
        · 링크 클릭 : {:,.0f} Clicks
        · CTR : {:.2%}
        · CPM : {:,.0f}원
        · CPC : {:,.0f}원
        · 링크 클릭 CPC : {:,.0f}원
        · CPI : {:,.0f}원
        · 컨텐츠 반응 : {:,} Like / {:,} Page Like / {:,} Share / {:,} Comment

        · 관심사 타겟 정보 :

        <운영 코멘트>
        · 
        · CTR {:.2%}, CPC {:,.0f}원, CPI {:,.0f}원, CPM {:,.0f}원
        · 
        · 


        """.format(
                        num,
                        gubun.replace('\n', ' ').replace("  ", ' ').replace("  ", ' ').strip(),
                        data['날짜'].replace('\n', ' '),
                        hyphen_to_zero(data['노출']),
                        hyphen_to_zero(data['클릭']),
                        hyphen_to_zero(data['링크클릭']),
                        hyphen_to_floatzero(data['CTR']),
                        hyphen_to_floatzero(data['CPM']),
                        hyphen_to_floatzero(data['CPC']),
                        hyphen_to_floatzero(data['링크클릭CPC']),
                        hyphen_to_floatzero(data['CPI(인터렉션)']),
                        hyphen_to_zero(data['Reaction(Like)']),
                        hyphen_to_zero(data['Reaction(PageLike)']),
                        hyphen_to_zero(data['Reaction(Share)']),
                        hyphen_to_zero(data['Reaction(Comment)']),
                        hyphen_to_floatzero(data['CTR']),
                        hyphen_to_floatzero(data['CPC']),
                        hyphen_to_floatzero(data['CPI(인터렉션)']),
                        hyphen_to_floatzero(data['CPM']),
                    )
            #         print(element)
                    body += element
                    num += 1
                else:
                    element = """{}. {:} : {:}

        <지표 성과>
        · 달성 노출 : {:,.0f} Imps
        · 달성 클릭 : {:,.0f} Clicks
        · CTR : {:.2%}
        · CPM : {:,.0f}원
        · CPC : {:,.0f}원
        · CPI : {:,.0f}원
        · 컨텐츠 반응 : {:,} Like / {:,} Page Like / {:,} Share / {:,} Comment

        · 관심사 타겟 정보 :

        <운영 코멘트>
        · 
        · CTR {:.2%}, CPC {:,.0f}원, CPI {:,.0f}원, CPM {:,.0f}원
        · 
        · 


        """.format(
                        num,
                        gubun.replace('\n', ' ').replace("  ", ' ').replace("  ", ' ').strip(),
                        data['날짜'].replace('\n', ' '),
                        hyphen_to_zero(data['노출']),
                        hyphen_to_zero(data['클릭']),
                        hyphen_to_floatzero(data['CTR']),
                        hyphen_to_floatzero(data['CPM']),
                        hyphen_to_floatzero(data['CPC']),
                        hyphen_to_floatzero(data['CPI(인터렉션)']),
                        hyphen_to_zero(data['Reaction(Like)']),
                        hyphen_to_zero(data['Reaction(PageLike)']),
                        hyphen_to_zero(data['Reaction(Share)']),
                        hyphen_to_zero(data['Reaction(Comment)']),
                        hyphen_to_floatzero(data['CTR']),
                        hyphen_to_floatzero(data['CPC']),
                        hyphen_to_floatzero(data['CPI(인터렉션)']),
                        hyphen_to_floatzero(data['CPM']),
                    )
            #         print(element)
                    body += element
                    num += 1



        # print(body)
        f = codecs.open(path +  'txt/' + '{}_{}_FB.txt'.format(day, week), 'w', encoding='cp949')
        f.write(body)
        f.close()
        print('{}_{}_FB.txt'.format(day, week), '생성 완료')
    except FileNotFoundError as e:
        print(e)
        print("Facebook 리포트가 없습니다.")
    body = body.replace("\n", "<br>")
    return body




def rw(day, path, today, yesterday):
    def rw_colname(columns):
        dic = {
            'CPI' : "인스타그램",
            "CPY" : "유튜브",
            "CPL" : "페이스북",
        }
        new_columns = []
        for colname in columns:
            for key in dic.keys():
                if key in colname:
                    new_columns.append("{} - {}".format(dic[key], colname))
        return new_columns
    try:
        filepath = path + 'report.xlsx'
        rw = pd.read_excel(filepath, sheet_name = 'Summary({}월)'.format(today.month), header = 3)
        rw = rw.iloc[:, :]
        rw = rw.set_index('플랫폼')
        # rw.columns = rw_colname(rw.columns)
        # rw = rw.dropna(axis=0, how='all')
        # rw = rw.fillna(axis=1, method='ffill')

        df = rw

        gubun = ''
        num = 1
        body = """안녕하세요,
퀀텀파이러츠 김소영입니다.

{y}년 {m}월 {d}일 리워드광고 Daily Report 전달드립니다.
리포트는 전일({yesterday})까지 수치 기입하였습니다. 참고 부탁드립니다.

---- 

[자사 리워드광고 효율 분석]  


    """.format(
    y = today.year,
    m = today.month,
    d = today.day,
    yesterday = yesterday.strftime('%m월 %d일')
    )

        media = df.columns
        for idx, medium in enumerate(media):
            element = """{num}. {medium} - {product}

<지표 성과>
· 집행 기간 : {start} ~ {end}
· 전환수 : {conv:,}
· 실전환수 : {conv_real:,}
· {m}월 잔존율 : {remaining_rate:.2%}
· {m}월 목표 달성률 : {accomplished_rate:.2%}

<운영 코멘트>
· {m}월 잔존율 {remaining_rate:.2%}로 ... 효율 나타났습니다.
· 현재 팬 수는 {fan:,}명 입니다.
· {m}월 목표 달성률 {accomplished_rate:.2%} 입니다.

    """.format(
                num = num,
                medium = medium,
                m = today.month,
                product = df.loc['매체명/상품', medium],
                start = df.loc['집행 시작일', medium].strftime("%Y.%m.%d"),
                end = df.loc['집행 종료일', medium].strftime("%Y.%m.%d"),
                conv = hyphen_to_zero(df.loc['전환수', medium]),
                conv_real = hyphen_to_zero(df.loc['실제 전환수(추정치)', medium]),
                remaining_rate = hyphen_to_floatzero(df.loc["기간 총 잔존율", medium]),
                accomplished_rate = hyphen_to_floatzero(df.loc["목표 달성률(7월)", medium]),
                fan = hyphen_to_zero(df.loc["팬 수({}기준)".format(yesterday.strftime("%m/%d")), medium])
    #             ee = df.loc['기간 총 잔존율', medium],
    #             ff = df.loc['목표 달성률({}월)'.format(today.month), medium],
    #             remaining_rate = df.loc["기간 총 잔존율".format(yesterday.strftime("%m"), yesterday.strftime("%d")), medium],
                )
            body += element
            num += 1
        body += """[경쟁사 분석 - 신한카드]\n 
1. 인스타그램

<모니터링 코멘트>
· 팔로워 감소 추이 이어졌으나 4월 시작과 함께 수치 급상승하였습니다.
· 최근 30일 실적 현재 시점까지 ,명 증가한 상황이며, 일 평균 ,명 증가하고 있습니다.
· 전일 명 증가했습니다.


2. 유튜브

<모니터링 코멘트>
· 팔로워 증가 추이 계속되고 있습니다.
· 최근 30일 실적 현재 시점까지 ,명 증가한 상황이며, 일 평균 명 증가하고 있습니다.
· 전일 명 증가했습니다.


3. 페이스북

<모니터링 코멘트>
· 팔로워 소량 증가 혹은 감소 추이 이어지고 있습니다.
· 최근 30일 실적 현재 시점까지 ,명 증가한 상황이며, 일 평균 명 증가하고 있습니다.
· 전일 명 증가/감소했습니다.


데일리리포트 관련하여 자세한 사항은 아래 첨부파일 확인 부탁드립니다.

감사합니다.
김소영 드림

        """
        f = codecs.open(path + 'txt/' + '{}_RW.txt'.format(day), 'w', encoding='cp949')
        f.write(body)
        f.close()

        print('RW.txt'.format(day), '생성 완료')

    except FileNotFoundError as e:
        print(e)
        print("해당 리포트가 없습니다.")
        return "잘못된 리포트입니다."

    # print(body)
    
    body = body.replace("\n", "<br>")
    return body