from __future__ import unicode_literals
import os
import shutil
import json
import youtube_dl2 as youtube_dl

def get_descriptions(urls):
    os.mkdir('files')

    ydl_opts = {
        'writedescription' : True,
        'skip_download' : True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

    filelist = os.listdir('files')
    print('filelist: ', filelist, '\n')
    data = []
    for filename in filelist:
        f = open('files/' + filename, 'r')
        text = f.read()
        print('text: ', text, '\n')
        data.append(text)
        f.close()

    try:
        shutil.rmtree('files')
    except OSError as e:
        if e.errno == 2:
            # 파일이나 디렉토리가 없음!
            print('No such file or directory to remove')
            pass
        else:
            raise
    return data