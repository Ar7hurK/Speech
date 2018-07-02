# -*- coding: utf-8 -*-

import pyaudio
import wave
import json
import requests
import base64
from tkinter import *

""" 你的 APPID AK SK """
APP_ID = '你的 App ID'
API_KEY = '你的 Api Key'
SECRET_KEY = '你的 Secret Key'


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token'
    grant_type = 'client_credentials'
    data = {'grant_type': grant_type, 'client_id': API_KEY, 'client_secret': SECRET_KEY}
    response = requests.post(host, data)
    token = response.json()['access_token']
    return token


def recognize(audio, token):
    url = 'http://vop.baidu.com/server_api'
    size = len(audio)
    data = {
        "format": "wav",
        "rate": 16000,
        "dev_pid": 1536,
        "channel": 1,
        "token": token,
        "cuid": APP_ID,
        "len": size,
        "speech": base64.b64encode(audio).decode('utf8'),
    }
    result = requests.post(url, json.dumps(data))
    rs = result.json()
    return rs


def ns():
    filePath = 'audio/output.wav'
    token = get_token()
    audio = get_file_content(filePath)
    rs = recognize(audio, token)

    if rs['err_msg'] == 'success.':
        rt = "识别成功！\n" \
             "识别结果：" + str(rs['result'][0])
    else:
        rt = "识别失败！！！\n" \
             "错误码：" + str(rs['err_no']) + "\n" \
             "错误码描述：" + rs['err_msg']

    return rt


def rc():
    CHUNK = 1600
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "audio/output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* 录音开始")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* 录音结束")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def netspeech():
    List.delete(0.0, END)
    List.insert(END, '录音开始\n')
    List.update()
    rc()
    List.insert(END, '录音结束,正在识别,请耐心等待\n')
    List.update()
    text = ns()
    List.insert(END, '识别结果为:\n')
    List.insert(END, text)
    List.update()


if __name__ == '__main__':
    win = Tk()
    win.title('语音识别')
    button = Button(win, text='直接识别', width=15, command=netspeech)
    button.grid(row=1, column=1, padx=20, pady=20)
    List = Text(win)
    List.grid(row=2, column=1, padx=20, pady=20)
    win.mainloop()
