from __future__ import unicode_literals
import io
from contextlib import redirect_stdout

import youtube_dl


# 나중에 url list를 받는 것도 필요
def get_descriptions(urls):
    with io.StringIO() as buf, redirect_stdout(buf):
        ydl_opts = {
            'forcedescription' : True,
            'simulate' : True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # ydl.download([url])
            ydl.download(urls)
        output = buf.getvalue()
        # output = output.split('Downloading video info webpage\n')[1]
    return output

# url_list = ['https://www.youtube.com/watch?v=cF38IAyv3tg']
# desc = get_descriptions(url_list)
# desc = desc.split('Downloading video info webpage\n')[1]