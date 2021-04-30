# -*- coding: utf-8 -*-
# juliusを起動してから実行すること
"""
RaspberryPI3でスマートリモコン
"""
import subprocess
import socket
import string
import os
import random
import numpy as np
from numpy.random import *
import time

host = '127.0.0.1' 
port = 10500

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("input host port")
sock.connect((host, port))
print("connected")

data =""
killword =""

while True:
    
    if '</RECOGOUT>\n.' in data:    # 音声データの受信が完了している場合
        strTemp = ""
        for line in data.split('\n'):
            # 変換されたテキストとスコアを抽出する
            index = line.find('WORD="')
            if index != -1:
                line_ori = line
                line = line[index+6:line.find('"',index+6)] # テキストを取得
                if line == "[s]" or line == "[/s]":
                    continue
                cmscore = line_ori[-6:-3] # score値を取得 0.0% ~ 100.0%
                strTemp = str(line)
                print(cmscore)
                print(strTemp)
                cmscore = int(cmscore)
                if cmscore == 000:        # 100%は1000の下三桁で000が抽出されるので修正 
                    cmscore = 1000
            if strTemp == 'テレビオン' and int(cmscore) > 700:
                subprocess.Popen("python3 irrp.py -p -g17 -f codes light:on", shell = True)
                print("ON")
                break

            elif strTemp == 'テレビオフ'and int(cmscore) > 900:
                print("OFF")
                break

            elif strTemp == 'テレビいちばん' and int(cmscore) > 850:
                subprocess.Popen("python3 irrp.py -p -g17 -f ch1 light:on", shell = True)
                print("CH1")
                break

            elif strTemp == 'テレビにばん' and int(cmscore) > 850:
                subprocess.Popen("python3 irrp.py -p -g17 -f ch2 light:on", shell = True)
                print("CH2")
                break

            elif strTemp == 'テレビさんばん' and int(cmscore) > 850:
                subprocess.Popen("python3 irrp.py -p -g17 -f ch3 light:on", shell = True)
                print("CH3")
                break
            
            elif strTemp == 'テレビよんばん' and int(cmscore) > 800:
                subprocess.Popen("python3 irrp.py -p -g17 -f ch4 light:on", shell = True)
                print("CH4")
                break

            elif strTemp == 'テレビごばん' and int(cmscore) > 850:
                subprocess.Popen("python3 irrp.py -p -g17 -f ch5 light:on", shell = True)
                print("CH5")
                break

            elif strTemp == 'テレビろくばん' and int(cmscore) > 900:
                subprocess.Popen("python3 irrp.py -p -g17 -f ch6 light:on", shell = True)
                print("CH6")
                break
            
            elif strTemp == '消灯して' and int(cmscore) > 990:
                subprocess.Popen("python3 irrp.py -p -g17 -f lightoff light:on", shell = True)
                break

            elif strTemp == '点灯して' and int(cmscore) > 990:
                subprocess.Popen("python3 irrp.py -p -g17 -f lighton light:on", shell = True)
                break

            elif strTemp == 'エアコン付けて' and int(cmscore) > 990:
                subprocess.Popen("python3 irrp.py -p -g17 -f danbou light:on", shell = True)
                break

            elif strTemp == 'エアコン消して' and int(cmscore) > 990:
                subprocess.Popen("python3 irrp.py -p -g17 -f airoff light:on", shell = True)
                break

            else:
                pass
            # 処理済みのデータを削除する
            data = ""
            
    else:   # 音声データを受信完了していない場合、受信されているデータを追加する
        data += str(sock.recv(1024).decode('utf-8'))
