def run(week, day)
    print('cr.run once')
    path = './user_upload/'
    rw_file = path + 'report.xlsx'

    import sys
    import pandas as pd
    import numpy as np
    import codecs

    def hyphen_to_zero(hyphen_like):
        return int(str(hyphen_like).replace('-', '0').replace('.0', ''))

    def hyphen_to_floatzero(hyphen_like):
        return float(str(hyphen_like).replace('-', '0'))


    fb_file = path + '[QP] 현대카드_Facebook 콘텐츠광고_Daily Report_{}.xlsx'.format(day)
    ig_file = path + '[QP] 현대카드_Instagram 콘텐츠광고_Daily Report_{}.xlsx'.format(day)
    yt_file = path + '[QP] 현대카드_Youtube 콘텐츠 광고 Daily Report_{}.xlsx'.format(day)


    # YT 전처리
    try:
        today = datetime.strptime(day, "%y%m%d").date()
        yesterday = today - timedelta(days=1)

        rw = pd.read_excel(rw_file, sheet_name = '매체별효율_{}월'.format(today.month), header = 3)
        rw = rw.iloc[:, 1:4]
        rw = rw.set_index('플랫폼')

        yt = pd.read_excel(yt_file, sheet_name = week, header = 3)
        yt = yt.iloc[1:, :]
        yt.columns = [
            '구분', '날짜', '소재', '광고타겟', '예산(vat포함)', '예산', '소진금액', 
            '소진금액(vat포함)', '노출', '클릭', '조회', 'CTR', 'VTR', 
            'CPC', 'CPV', '영상 재생률 25%', '영상 재생률 50%', '영상 재생률 75%', 
            '영상 재생률 100%', '영상 좋아요', '채널 구독', '링크'
        ]
        yt = yt.reset_index(drop=True)
        yt = yt.fillna(method='ffill')

    # YT PRINT
        df = yt
        df_pretty_print(df)

        gubun = ''
        num = 1
        body = ''

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
    · CPV : {:,.0f}원
    · 동영상 재생진행률
        - 25% : {:.2%}
        - 50% : {:.2%}
        - 75% : {:.2%}
        - 100% : {:.2%}


    """.format(
                    num,
                    gubun.replace('\n', ' ').replace("  ", ' ').replace("  ", ' ').strip(),
                    data['날짜'].replace('\n', ' '),
                    hyphen_to_zero(data['노출']),
                    hyphen_to_zero(data['조회']),
                    hyphen_to_floatzero(data['VTR']),
                    hyphen_to_floatzero(data['CPV']),
                    hyphen_to_floatzero(data['영상 재생률 25%']),
                    hyphen_to_floatzero(data['영상 재생률 50%']),
                    hyphen_to_floatzero(data['영상 재생률 75%']), 
                    hyphen_to_floatzero(data['영상 재생률 100%']),
                )
        #         print(element)
                body += element
                num += 1

        # print(body)
        f = codecs.open(path + 'txt/' + '{}_{}_YT.txt'.format(day, week), 'w', encoding='cp949')
        f.write(body)
        f.close()
        print('{}_{}_YT.txt'.format(day, week), '생성 완료')
    except FileNotFoundError as e:
        print(e)
        print("Youtube 리포트가 없습니다.")




    # FB 전처리
    try:
        fb = pd.read_excel(fb_file, sheet_name = week, header = 3)
        fb = fb.iloc[1:, :]
        fb.columns = ['구분', '날짜', '소재', '광고 타겟', '모수', '예산(vat포함)', '예산', '소진금액',
            '소진 금액(vat포함)', '광고도달', '노출', '클릭', 'CTR',
            'CPC', 'CPL', '링크클릭', '링크클릭CPC', 'CPV',
            'Video Views (3초+)', 'Video Views (100%)',
            'CPI(인터렉션)', 'Reaction(Like)', 'Reaction(PageLike)', 'Reaction(Share)', 
                    'Reaction(Comment)', 'Reaction(Total)', '링크']
        fb = fb.fillna(method='ffill')
        fb = fb.reset_index(drop=True)

    # FB PRINT
        df = fb
        df_pretty_print(df)

        gubun = ''
        num = 1
        body = ''
        for row in df.iloc[:, :].iterrows():
            data = row[1]
            if data['구분'] != '합계/평균':
                gubun = data['구분']
            elif data['구분'] == '합계/평균':
                element = """{}. {:} : {:}

    <지표 성과>
    · 달성 노출 : {:,.0f} Imps
    · 달성 클릭 : {:,.0f} Clicks
    · CTR : {:.2%}
    · CPC : {:,.0f}원
    · CPI : {:,.0f}원
    · 컨텐츠 반응 : {:,} Like / {:,} Page Like / {:,} Share / {:,} Comment


    """.format(
                    num,
                    gubun.replace('\n', ' ').replace("  ", ' ').replace("  ", ' ').strip(),
                    data['날짜'].replace('\n', ' '),
                    hyphen_to_zero(data['노출']),
                    hyphen_to_zero(data['클릭']),
                    hyphen_to_floatzero(data['CTR']),
                    hyphen_to_floatzero(data['CPC']),
                    hyphen_to_floatzero(data['CPI(인터렉션)']),
                    hyphen_to_zero(data['Reaction(Like)']),
                    hyphen_to_zero(data['Reaction(PageLike)']),
                    hyphen_to_zero(data['Reaction(Share)']),
                    hyphen_to_zero(data['Reaction(Comment)'])
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


    # IG 전처리
    try:
        ig = pd.read_excel(ig_file, sheet_name = week, header = 3)
        ig = ig.iloc[1:, :]
        ig.columns = ['구분', '날짜', '소재', '광고 타겟', '모수', '예산(vat포함)', '예산', '소진금액',
            '소진 금액(vat포함)', '광고도달', '노출', '클릭', 'CTR',
            'CPC', '링크클릭', '링크클릭CPC', 'CPV',
            'Video Views (3초+)', 'Video Views (100%)', '페이지 Like', 'CPL',
            'CPI(인터렉션)', 'Reaction(Like)', 'Reaction(Share)', 'Reaction(Comment)', 
                    'Reaction(Total)', '링크']
        ig = ig.fillna(method='ffill')
        ig = ig.reset_index(drop=True)

    # IG PRINT
        df = ig
        df_pretty_print(df)

        gubun = ''
        num = 1
        body = ''
        for row in df.iloc[:, :].iterrows():
            data = row[1]
            if data['구분'] != '합계/평균':
                gubun = data['구분']
            elif data['구분'] == '합계/평균':
                element = """{}. {:} : {:}

    <지표 성과>
    · 달성 노출 : {:,} Imps
    · 달성 클릭 : {:,} Clicks
    · CTR : {:.2%}
    · CPC : {:,.0f}원
    · CPI : {:,.0f}원
    · 컨텐츠 반응 : {:,} Like / {:,} Share / {:,} Comment


    """.format(
                num,
                gubun.replace('\n', ' ').replace("  ", ' ').replace("  ", ' ').strip(),
                data['날짜'].replace('\n', ' '),
                hyphen_to_zero(data['노출']),
                hyphen_to_zero(data['클릭']),
                hyphen_to_floatzero(data['CTR']),
                hyphen_to_floatzero(data['CPC']),
                hyphen_to_floatzero(data['CPI(인터렉션)']),
                hyphen_to_zero(data['Reaction(Like)']),
                hyphen_to_zero(data['Reaction(Share)']),
                hyphen_to_zero(data['Reaction(Comment)'])
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
