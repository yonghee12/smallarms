import hcc_functions

def run(medium, day, week):
    path = './user_upload/'
    filepath = path + 'report.xlsx'

    import sys
    import pandas as pd
    import numpy as np
    import codecs

    from datetime import date
    from datetime import timedelta
    from datetime import datetime

    import urllib

    today = datetime.strptime(day, "%y%m%d").date()
    yesterday = today - timedelta(days=1)
    
    if medium == 'rw':
        return hcc_functions.rw(day, path, today, yesterday)
    elif medium == 'yt':
        return hcc_functions.yt(day, path, week, today, yesterday)
    elif medium == 'ig':
        return hcc_functions.ig(day, path, week, today, yesterday)
    elif medium == 'fb':
        return hcc_functions.fb(day, path, week, today, yesterday)
    else:
        print('Nothing Passed')


    # def yt(day, filepath):
    #     try:
    #         yt = pd.read_excel(filepath, sheet_name = "2월 18주", header = 3)
    #         yt = yt.iloc[1:, :]
    #         yt.columns = [
    #             '구분', '날짜', '소재', '광고타겟', '예산(vat포함)', '예산', '소진금액', 
    #             '소진금액(vat포함)', '노출', '클릭', '조회', 'CTR', 'VTR', 
    #             'CPC', 'CPV', '영상 재생률 25%', '영상 재생률 50%', '영상 재생률 75%', 
    #             '영상 재생률 100%', '영상 좋아요', '채널 구독', '링크'
    #         ]
    #         yt = yt.reset_index(drop=True)
    #         yt = yt.fillna(method='ffill')

    #     # YT PRINT
    #         df = yt
    #         df_pretty_print(df)

    #         gubun = ''
    #         num = 1
    #         body = ''

    #         for row in df.iloc[:, :].iterrows():
    #             data = row[1]
    #             if data['구분'] != '합계/평균':
    #                 gubun = data['구분']
    #                 continue
    #             elif data['구분'] == '합계/평균':
    #                 element = """{}. {:} : {:}

    #     <지표 성과>
    #     · 달성 노출 : {:,} Imps
    #     · 달성 조회 : {:,} View
    #     · VTR : {:.2%}
    #     · CPV : {:,.0f}원
    #     · 동영상 재생진행률
    #         - 25% : {:.2%}
    #         - 50% : {:.2%}
    #         - 75% : {:.2%}
    #         - 100% : {:.2%}


    #     """.format(
    #                     num,
    #                     gubun.replace('\n', ' ').replace("  ", ' ').replace("  ", ' ').strip(),
    #                     data['날짜'].replace('\n', ' '),
    #                     hyphen_to_zero(data['노출']),
    #                     hyphen_to_zero(data['조회']),
    #                     hyphen_to_floatzero(data['VTR']),
    #                     hyphen_to_floatzero(data['CPV']),
    #                     hyphen_to_floatzero(data['영상 재생률 25%']),
    #                     hyphen_to_floatzero(data['영상 재생률 50%']),
    #                     hyphen_to_floatzero(data['영상 재생률 75%']), 
    #                     hyphen_to_floatzero(data['영상 재생률 100%']),
    #                 )
    #         #         print(element)
    #                 body += element
    #                 num += 1

    #         # print(body)
    #         f = codecs.open(path + 'txt/' + '{}_{}_YT.txt'.format(day, week), 'w', encoding='cp949')
    #         f.write(body)
    #         f.close()
    #         print('{}_{}_YT.txt'.format(day, week), '생성 완료')

    #     except FileNotFoundError as e:
    #         print(e)
    #         print("해당 리포트가 없습니다.")
    #         return "잘못된 리포트입니다."

    #         # print(body)
            
    #     body = body.replace("\n", "<br>")
    #     return body



    # def rw(day, filepath):
    #     try:
    #         rw = pd.read_excel(filepath, sheet_name = '매체별효율_{}월'.format(today.month), header = 3)
    #         rw = rw.iloc[:, 1:4]
    #         rw = rw.set_index('플랫폼')

    #         df = rw

    #         gubun = ''
    #         num = 1
    #         body = """{y}년 {m}월 {d}일 인스타그램, 유튜브 리워드광고 Daily Report 전달드립니다.
    # 리포트는 전일({ym}월 {yd}일)까지 수치 기입하였습니다. 참고 부탁드립니다.

    # """.format(
    #         y = today.year,
    #         m = today.month,
    #         d = today.day,
    #         ym = yesterday.month,
    #         yd = yesterday.day,
    #         )

    #         media = df.columns
    #         for idx, medium in enumerate(media):
    #             element = """{num}. {medium} - {product}

    # <지표 성과>
    # · 집행 기간 : {aa}
    # · 일일 전환수 : {bb:,}
    # · 일일 실전환수 : {cc:,}
    # · 당일 잔존율 : {dd:.2%}
    # · {m}월 잔존율 : {ee:.2%}
    # · {m}월 목표 달성율 : {ff:.2%}

    # <운영 코멘트>

    # """.format(
    #                 num = num,
    #                 medium = medium,
    #                 m = today.month,
    #                 product = df.loc['매체명/상품', medium],
    #                 aa = df.loc['(집행 기간)', medium],
    #                 bb = df.loc['일일 리워드 전환수', medium],
    #                 cc = df.loc['일일 실제 전환수', medium],
    #                 dd = df.iloc[11, idx],
    #                 ee = df.loc['기간 총 잔존율', medium],
    #                 ff = df.loc['목표 달성률({}월)'.format(today.month), medium],
    #                 )
    #             # element = element.replace(u'\xa0', u' ')
    #             body += element
    #             num += 1

    #         f = codecs.open(path + 'txt/' + '{}_RW.txt'.format(day), 'w', encoding='cp949')
    #         f.write(body)
    #         f.close()

    #         print('RW.txt'.format(day), '생성 완료')

    #     except FileNotFoundError as e:
    #         print(e)
    #         print("해당 리포트가 없습니다.")
    #         return "잘못된 리포트입니다."

    #     # print(body)
        
    #     body = body.replace("\n", "<br>")
    #     return body