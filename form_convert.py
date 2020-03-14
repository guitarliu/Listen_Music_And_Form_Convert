# -*- coding:utf-8 -*-

from tkinter import *

from tkinter.messagebox import *

from tkinter.filedialog import *

import cloudconvert, threading, random

from fake_useragent import UserAgent

import requests, io, pygame

from pygame import mixer

from urllib.parse import quote






root = Tk()

root.title("音乐下载及格式转换v1.0")

# 获得网易云音乐板块

# get请求直接下载, 链接：http://music.163.com/song/media/outer/url?id=歌曲id.mp3

# get请求歌曲，链接：http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=歌曲名称&type=1&offset=0&total=true&limit=搜索条数

class Music_Get(object):

    def __init__(self):

        self.ua = UserAgent(verify_ssl=False)

        self.search_headers = {

            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

            'Accept-Encoding': 'gzip, deflate',

            'Accept-Language': 'zh-CN,zh;q=0.9',

            'Cache-Control': 'max-age=0',

            'Connection': 'keep-alive',

            'Host': 'music.163.com',

            'Upgrade-Insecure-Requests': '1',

            'User-Agent': self.ua.random
        }

    def search_music(self):

        if e_song_name.get() == '':

            showwarning(title='歌名未输入！', message='请输入要搜索的歌名')

        else:

            count = 1

            global list_song_info

            list_song_info = []

            song_name_url_encode = quote(e_song_name.get())

            song_get_pages_url = 'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=%s&type=1&offset=0&total=true&limit=30' % song_name_url_encode

            resp_pages = requests.get(song_get_pages_url, headers=self.search_headers)

            search_result = resp_pages.json()

            songs_info = search_result['result']['songs']

            global v

            v = IntVar()

            v.set(1)

            top = Toplevel(bg='#FAFAD2')

            top.title('音乐列表')

            Button(top, text='退出', activebackground='#00BFFF', command=top.destroy).pack(side=BOTTOM, pady=20)

            Button(top, text='下载', activebackground='#00BFFF', command=Music_Get().download_music).pack(anchor=CENTER, pady=2)

            for song_info in songs_info:

                if song_info['alias'] == []:

                    song_info['alias'] = ''

                else:

                    song_info['alias'] = song_info['alias'][0]

                single_song = song_info['name'] + song_info['alias']

                songer = song_info['artists'][0]['name']

                song_album = song_info['album']['name']

                song_id = str(song_info['id'])

                content = single_song.ljust(10) + '\t' + songer.ljust(10) + '\t' + song_album.ljust(10) + '\t' + song_id

                list_song_info.append((content, count))

                count += 1

            for lang, num in list_song_info:

                b = Radiobutton(top, text=lang, variable=v, value=num, bg='#FAFAD2', command=Music_Get().select_music)

                b.pack(anchor=W)

    def download_music(self):
        """
        下载音乐，并保存在指定的文件夹
        """
        global v, list_song_info

        song_id = list_song_info[v.get()-1][0].split('\t')[-1]

        music_filename = asksaveasfilename(title='保存音乐', filetypes=[('MP3', '.mp3')])

        url = 'http://music.163.com/song/media/outer/url?id=%s.mp3' % song_id

        resp = requests.get(url, headers={'User-Agent': self.ua.random})

        with open(music_filename, 'wb') as f:

            f.write(resp.content)

        showinfo(title='下载提示', message='歌曲%s下载完成！' % e_song_name.get())

    def select_music(self):
        """
        选中音乐后弹窗播放
        """
        top_play = Toplevel(bg='#FAFAD2')

        top_play.title('播放按钮')

        Message(top_play, text='每次选中一首歌会弹出一个播放窗口,记得换歌播放时关闭这个窗口,退出这个窗口不会停止播放', bg='#6495ED', relief=GROOVE).pack(side=LEFT)

        Button(top_play, text='播放', activebackground='#00BFFF', command=Music_Get().play_music).pack(side=LEFT, padx=2, pady=2)

        Button(top_play, text='停止', activebackground='#00BFFF', command=Music_Get().stop_play).pack(side=LEFT, padx=2,
                                                                                                    pady=2)
        Button(top_play, text='退出', activebackground='#00BFFF', command=top_play.destroy).pack(side=LEFT, padx=2, pady=2)

    def play_music(self):
        """
        播放选中的音乐
        """
        global v, list_song_info

        song_id = list_song_info[v.get() - 1][0].split('\t')[-1]

        url_music = 'http://music.163.com/song/media/outer/url?id=%s.mp3' % song_id

        resp_content = requests.get(url_music, headers={'User-Agent': self.ua.random})

        play_content = io.BytesIO(resp_content.content)

        pygame.mixer.init()

        pygame.mixer.music.load(play_content)

        pygame.mixer.music.play()

    def stop_play(self):

        pygame.mixer.music.stop()









form_music = LabelFrame(root, text="音乐下载", padx=5, pady=5, bg='#FAFAD2', width=600, height=200)

form_music.pack(padx=2, pady=1)

Message(form_music, text='音乐下载模块的主要功能为\n      (1)搜索并生成按钮列表\n      (2)用户选择列表单曲保存\n功能缺点\n      (1)无法多首歌曲同时下载\n      (2)弹出多个窗口无法替换', bg='#6495ED', width=200, relief=GROOVE).pack(side=LEFT)

Label(form_music, text="歌曲名", bg='#FAFAD2').pack(side=LEFT, padx=5, pady=3)

e_song_name = Entry(form_music, width=20)

e_song_name.pack(side=LEFT, pady=5)

Button(form_music, text='搜索', activebackground='#00BFFF', command=Music_Get().search_music).pack(side=LEFT, padx=5, pady=5)

Button(form_music, text='退出', activebackground='#00BFFF', command=root.quit).pack(side=LEFT, padx=5, pady=5)



# 格式转换板块

form_convert = LabelFrame(root, text="格式转化", padx=5, pady=5, bg='#FAFAD2', width=600, height=200)

form_convert.pack(padx=2, pady=2)

Message(form_convert,
        text="注意: 这个软件使用的账号为免费账号，只享有以下功能:\n\n\t(1) 最大转换文件1GB\n\n\t(2) 每次最大转换数5\n\n\t(3) 每天使用25min", bg='#6495ED', relief=GROOVE).pack(
    side=LEFT)

w = Canvas(form_convert, width=10, height=150, bg="#FAFAD2")

w.create_line(10, 0, 10, 200, fill='#9370DB')

w.pack(side=LEFT)


def upload_file():
    """
    上传文件
    """
    fileName = askopenfilename(title="上传文件")

    v_filename.set(fileName)

    v_file_format.set(fileName.split("/")[-1].split('.')[-1])


# 上传文件按钮

v_file_format = StringVar()

v_filename = StringVar()

v_savefile = StringVar()

Button(form_convert, text="上传文件", activebackground='#00BFFF', command=upload_file).pack(side=LEFT, padx=5, pady=3)

Label(form_convert, text="文件格式为:", bg='#FAFAD2', padx=1, pady=5).pack(side=LEFT, padx=5, pady=3)

Label(form_convert, textvariable=v_file_format, padx=5, pady=5, bg='#FAFAD2').pack(side=LEFT, padx=5, pady=3)

Label(form_convert, text="转换为", bg='#FAFAD2', padx=2, pady=5).pack(side=LEFT, padx=5, pady=3)

list_formats = [

    '7z', 'ace', 'alz', 'arc', 'arj', 'bz', 'bz2', 'cab', 'cpio',

    'deb', 'dmg', 'eml', 'gz', 'img', 'iso', 'jar', 'lha', 'lz',

    'lzma', 'lzo', 'rar', 'rpm', 'rz', 'tar', 'tar.7z', 'tar.bz',

    'tar.bz2', 'tar.gz', 'tar.lzo', 'tar.xz', 'tar.Z', 'tbz',

    'tbz2', 'tgz', 'tZ', 'tzo', 'xz', 'z', 'zip', 'aac', 'ac3',

    'aif', 'aifc', 'aiff', 'amr', 'au', 'caf', 'flac', 'm4a',

    'm4b', 'mp3', 'oga', 'ogg', 'sf2', 'sfark', 'voc', 'wav',

    'weba', 'wma', 'dwg', 'dxf', 'abw', 'djvu', 'doc', 'docm',

    'docx', 'html', 'lwp', 'md', 'odt', 'pages', 'pages.zip',

    'pdf', 'rst', 'rtf', 'sdw', 'tex', 'txt', 'wpd', 'wps', 'zabw',

    'azw', 'azw3', 'azw4', 'cbc', 'cbr', 'cbz', 'chm', 'docx',

    'epub', 'fb2', 'htm', 'html', 'htmlz', 'lit', 'lrf', 'mobi',

    'odt', 'oeb', 'pdb', 'pdf', 'pml', 'prc', 'rb', 'rtf', 'snb',

    'tcr', 'txt', 'txtz', 'eot', 'otf', 'ttf', 'woff', '3fr', 'arw',

    'bmp', 'cr2', 'crw', 'dcr', 'dng', 'eps', 'erf', 'gif', 'heic',

    'icns', 'ico', 'jpeg', 'jpg', 'mos', 'mrw', 'nef', 'odd', 'orf',

    'pdf', 'pef', 'png', 'ppm', 'ps', 'psd', 'raf', 'raw', 'svg',

    'svgz', 'tif', 'tiff', 'webp', 'x3f', 'xcf', 'xps', 'dps',

    'eps', 'html', 'key', 'key.zip', 'odp', 'pdf', 'pps', 'ppsx',

    'ppt', 'pptm', 'pptx', 'ps', 'sda', 'swf', 'csv', 'et', 'html',

    'numbers', 'numbers.zip', 'ods', 'pdf', 'sdc', 'xls', 'xlsm',

    'xlsx', 'ai', 'cdr', 'cgm', 'emf', 'eps', 'pdf', 'ps', 'sk',

    'sk1', 'svg', 'svgz', 'vsd', 'wmf', '3g2', '3gp', '3gpp', 'avi',

    'cavs', 'dv', 'dvr', 'flv', 'gif', 'm2ts', 'm4v', 'mkv', 'mod',

    'mov', 'mp4', 'mpeg', 'mpg', 'mts', 'mxf', 'ogg', 'rm', 'rmvb',

    'swf', 'ts', 'vob', 'webm', 'wmv', 'wtv', 'website'
]

# 下拉滚动条，显示格式种类

sb = Scrollbar(form_convert, repeatdelay=100, bg='#FAFAD2')

lb = Listbox(form_convert, width=5, height=5, yscrollcommand=sb.set, relief=GROOVE)

for i in list_formats:

    lb.insert(END, i)

lb.pack(side=LEFT, fill=BOTH)

sb.pack(side=LEFT, fill=Y)

sb.config(command=lb.yview)




def process_convert(inputformat, outputformat, inputfile, save_filename):
    """
    创建一个process转换格式并把文件下载下来
    :param inputfile: 上传文件路径
    :param save_filename: 保存的文件名(含文件路径)
    :param inputformat: 上传的文件格式
    :param outputformat: 目标格式
    """
    API_KEY = random.choice([

        'DbCqLbhEnDyhIqFv1rvqEyrunYSirQQSjpCTiLJ5IjUwPdj3Wba5nT0SJ77jN3oO',

        'J1WZq6CVKnp3XmDNmCoJVxYLoRBtD02xlQW9nx27HzVoAvcflbsXY3mjyXgKTTCF',

    ])

    api = cloudconvert.Api(api_key=API_KEY)

    process = api.convert({

        'inputformat': inputformat,

        'outputformat': outputformat,

        'input': 'upload',

        'file': open(inputfile, 'rb')
    })

    process.wait()

    process.download('%s' % save_filename)


def convert_form():
    """
    将已知格式的文件转换为目标格式
    """
    if lb.curselection() == ():

        showwarning(title="Warning", message="请选择一种格式!", icon=WARNING)

    elif v_file_format.get() == '':

        showwarning(title="Warning", message="请选择一个文件!", icon=WARNING)

    else:

        outputformat = lb.get(lb.curselection())

        save_filename = asksaveasfilename(title="保存文件", filetypes=[(outputformat, ".%s" % outputformat)])

        v_savefile.set(save_filename)

        for i in range(5):

            t = threading.Thread(target=process_convert, args=(v_file_format.get(), outputformat, v_filename.get(), v_savefile.get()))

            t.start()

        showinfo(title='正在进行格式转换(o^^o)',
                 message="老弟，我将%s转换为%s啦，快给我打钱！!" % (v_filename.get().split('/')[-1], outputformat))


Button(form_convert, text="转换", activebackground='#00BFFF', command=convert_form, padx=3).pack(side=RIGHT, padx=5,
                                                                                               pady=5)

mainloop()
