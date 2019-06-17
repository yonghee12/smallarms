from __future__ import unicode_literals
import os
import shutil
import json
import youtube_dl2 as youtube_dl

def get_time_sorted_filelist(filelist):
    filelist_with_time = []
    for filename in filelist:
        created_time = os.stat('files/' + filename).st_ctime
        print(filename, created_time)
        filelist_with_time.append((created_time, filename))
    filelist_with_time.sort(key = lambda element : element[0])
    return filelist_with_time

def get_descriptions(urls):
    try:
        os.mkdir('files')
    except FileExistsError:
        print("FILES FOLDER NOT DELETED")
        shutil.rmtree('files')
        os.mkdir('files')

    ydl_opts = {
        'writedescription' : True,
        'skip_download' : True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

    filelist = os.listdir('files')
    filelist = get_time_sorted_filelist(filelist)
    print('filelist: ', filelist, '\n')
    data = []
    for fileinfo in filelist:
        filename = fileinfo[1]
        f = open('files/' + filename, 'r')
        text = f.read()
        print('text: ', text, '\n')
        data.append(text)
        f.close()
    print('-----------\n', 'LENGTH', len(data), '\n-----------\n')

    # 생성된 폴더를 삭제
    try:
        shutil.rmtree('files')
    except OSError as e:
        if e.errno == 2:
            # 파일이나 디렉토리가 없음!
            print('No such file or directory to remove')
            pass
        else:
            raise
    print(data)
    return data