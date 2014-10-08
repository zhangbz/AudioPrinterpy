AudioPrinter
============
作品名称：AudioPrinter

作品描述：AudioPrinter是一款基于Linux平台开发的桌面应用。预期功能是实现大量语音信息的实时文字速记，甚至取代速记员这一职业。

开发平台：Ubuntu Linux
应用语言：c python shell
技术要点：python模块Tkinter,pyaudio,numpy,wave,threading,subprocess,讯飞语音云SDK,多线程.

演示平台：Ubuntu 12.04LTS ,python2.7 
操作说明（需要接入网路）：
step1:点击AudioPrinter图标，打开应用界面。（注：由于时间有限，并未完成完美的打包，若本机python没有numpy,pyaudio模块，请自行使用python模块文件夹中的脚本和软件包下载安装。）
step2:请确保在录音时安静状态下（录音过程中无语音输入）点击“测试阈值”（若使用麦克风等设备，请务必在点击前连接）。
step3:点击“开始录音”，开始录音。
step4:待录音结束，点击“结束录音”。语音和文本文件均以result为文件名保存在当前目录下。
step5:点击“打开文本”，打开文本，编辑并保存。
step6:可点击“播放录音”，辅助编辑工作。

特别提醒:理想状态下，转换结果的准确率可达97%，但由于使用环境，是否录音设备，设备性能，网络因素，语音自身因素等影响，转换结果准确率会有相应的下降。若现场演示效果欠佳，可参考演示视频。
