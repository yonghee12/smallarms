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