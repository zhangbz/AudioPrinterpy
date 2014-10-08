#!/usr/bin/env python
# coding=utf-8

from Tkinter import *
from pyaudio import PyAudio, paInt16
from random import randint 
from time import sleep
from datetime import datetime
import numpy as np
import wave
import threading
import subprocess

#字符常量
NUM_SAMPLES = 2000        #pyAudio内部缓存的块的大小
SAMPLING_RATE = 16000      #取样频率
COUNT_NUM = 20   #NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
SAVE_LENTH = 8            #声音记录的最小长度：SAVE_LENTH * NUM_SAMPLES个取样

#全局变量
FLAG = 0
BEGIN = 1
WAVELIST = []
LEVEL = 6000              #声音保存的阈值

#将data中的数据保存到名为filename的wav文件中
def save_wave_file(filename, data):

    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes("".join(data))
    wf.close()

#保存完整音频文件
def save_all_wave(stream):

    save_buffer1 = []
    global FLAG
    while FLAG:
        string_audio_data1 = stream.read(NUM_SAMPLES)
        save_buffer1.append(string_audio_data1)

    global BEGIN
    if BEGIN:
        filename1 = "result.wav"                 
        save_wave_file(filename1, save_buffer1)
        save_buffer1 = []



#处理音频输入流
def do_stream(stream):

    save_count = 0
    save_buffer = []
    global FLAG
    global LEVEL
    while FLAG:
        #读入NUM_SAMPLES个取样
        string_audio_data = stream.read(NUM_SAMPLES)
        #将读入的数据转换为数组
        audio_data = np.fromstring(string_audio_data, dtype = np.short)
        #计算大于LEVEL的取样的个数
        large_sample_count = np.sum( audio_data > LEVEL )
        print np.max(audio_data)
        #如果个数大于COUNT_NUM,则至少保存SAVE_LENGTH个块
        if large_sample_count > COUNT_NUM:
            save_count = SAVE_LENTH
        else:
            save_count -= 1

        if save_count < 0:
            save_count = 0

        if save_count > 0:
            #将要保存的数据放到save_buffer中
            save_buffer.append( string_audio_data )
        else:
            #将save_buffer中的数据写入wav文件，wav文件的文件名是保存的时刻
            if len(save_buffer) > 0:
                filename = './bin/wav/' + datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"                 
                save_wave_file(filename, save_buffer)
                global WAVELIST
                WAVELIST.append(filename)
                save_buffer = []
                print filename, "saved"

#转换函数
def wav2text():

    global FLAG
    global WAVELIST
    while FLAG:
        while WAVELIST:
            str = 'echo ' + WAVELIST[0] + '|./bin/iatdemo' 
            subprocess.call(str, shell = True)
            print WAVELIST[0],'has been wrote in the result.txt'
            WAVELIST = WAVELIST[1:]

class Gui(object):

    def __init__(self):
        self.top = Tk()
        self.top.title('Audio Printer')
        self.top.resizable(False, False)
        self.name_label = Label(self.top, text = 'Audio Printer v1.1')
        self.name_label.pack()

        self.canvas_frame = Frame(self.top)
        self.audio_canvas = Canvas(self.canvas_frame, bg = 'black', height = '480', width = '640')
        self.points = []
        self.audio_canvas.pack()
        self.canvas_frame.pack()

        self.button_frame = Frame(self.top)
        self.testbutton = Button(self.button_frame, text = '阈值测试', command = self.voiceTest, activeforeground = 'green', activebackground = 'white')
        self.begin = Button(self.button_frame, text = '开始录音', command = self.beginRecord,
activeforeground = 'green', activebackground = 'white')
        self.open = Button(self.button_frame, text = '打开文本', command = self.openTxt, activeforeground = 'green', activebackground = 'white')
        self.end = Button(self.button_frame, text = '结束录音', command = self.endRecord, activeforeground = 'green', activebackground = 'white')
        self.open_wav = Button(self.button_frame, text = '播放录音', command = self.openWav, activeforeground = 'green', activebackground = 'white')
        self.testbutton.pack(side = LEFT)
        self.begin.pack(side = LEFT)
        self.open.pack(side = LEFT)
        self.open_wav.pack(side = LEFT)
        self.end.pack(side = LEFT)
        self.button_frame.pack()

    def voiceTest(self, ev = None):

        temp = 0
        self.patest = PyAudio()
        self.teststream = self.patest.open(format = paInt16, channels = 1, rate = SAMPLING_RATE, input = True, frames_per_buffer = NUM_SAMPLES)

        for i in range(30):
            self.string_audio_data = self.teststream.read(NUM_SAMPLES)
            self.audio_data = np.fromstring(self.string_audio_data, dtype = np.short)
            temp += np.max(self.audio_data)
        global LEVEL
        LEVEL = (temp / 30) * 2
        print LEVEL



    def beginRecord(self, ev = None):


        global BEGIN
        if BEGIN:
            BEGIN = 0
            #开启声音输入
            self.pa = PyAudio()
            self.stream = self.pa.open(format = paInt16, channels = 1, rate = SAMPLING_RATE, input = True, frames_per_buffer = NUM_SAMPLES)
            global FLAG
            FLAG = 1
        
            i = threading.Thread(target = do_stream, args = (self.stream,))
            o = threading.Thread(target = wav2text, args = ())
            ii = threading.Thread(target = save_all_wave, args = (self.stream,))
            s = threading.Thread(target =self.drawLine, args = ())
            o.start()
            i.start()
            ii.start()
            s.start()

    def endRecord(self, ev = None):

        sleep(5)
        global BEGIN
        BEGIN = 1
        global FLAG
        FLAG = 0
        if not FLAG:
            self.audio_canvas.create_rectangle(0, 0, 640, 480, fill = 'black')

    def openTxt(self, ev = None):

        subprocess.call('gedit result.txt ', shell = True)

    def drawLine(self):

        global FLAG
        while FLAG:
            self.points = [(x * 4, randint(80, 400)) for x in range(160)]
            self.audio_canvas.create_line(self.points, fill = 'green')
            sleep(0.5)

            t = threading.Thread(target = self.clearLine, args = ())
            t.start()
            t.join()


    def clearLine(self):

        global FLAG
        if FLAG:
            self.audio_canvas.create_line(self.points, fill = 'black')

    def openWav(self):

        chunk = 1024
        wf = wave.open(r"result.wav", 'rb')
        p = PyAudio()

        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()), channels = wf.getnchannels(), rate = wf.getframerate(), output = True)
        while True:
            data = wf.readframes(chunk)
            if data == "":break
            stream.write(data)

        stream.close()
        p.terminate()

def main():

    Gui()
    mainloop()

if __name__ == '__main__':

    main()
