'''
 ┌─────────────────────────────────────────────────────────────┐
 │┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐│
 ││Esc│!1 │@2 │#3 │$4 │%5 │^6 │&7 │*8 │(9 │)0 │_- │+= │|\ │`~ ││
 │├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┤│
 ││ Tab │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │{[ │}] │ BS  ││
 │├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┤│
 ││ Ctrl │ A │ S │ D │ F │ G │ H │ J │ K │ L │: ;│" '│ Enter  ││
 │├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────┬───┤│
 ││ Shift  │ Z │ X │ C │ V │ B │ N │ M │< ,│> .│? /│Shift │Fn ││
 │└─────┬──┴┬──┴──┬┴───┴───┴───┴───┴───┴──┬┴───┴┬──┴┬─────┴───┘│
 │      │Fn │ Alt │         Space         │ Alt │Win│   HHKB   │
 │      └───┴─────┴───────────────────────┴─────┴───┘          │
 └─────────────────────────────────────────────────────────────┘

Date         : 2017-02-21 12:43:08
LastEditors  : Stark1937
LastEditTime : 2023-02-07 20:01:31
FilePath     : /frida/run.py
'''

import sys
import frida
import codecs
import threading

global session

finished = threading.Event()
# 系统标准输出，支持grepÎ
def outWrite(text):
    sys.stdout.write(text.encode('utf8') + '\n');


# 带颜色打印输出
def colorPrint(color, s):
    return "%s[31;%dm%s%s[0m" % (chr(27), color, s, chr(27))


def get_usb_iphone():
    dManager = frida.get_device_manager();
    changed = threading.Event()

    def on_changed():
        changed.set()
    dManager.on('changed', on_changed)
    device = None
    while device is None:
        devices = [dev for dev in dManager.enumerate_devices() if dev.type == 'usb']
        if len(devices) == 0:
            print ('Waiting for usb device...')
            changed.wait()
        else:
            device = devices[0]

    dManager.off('changed', on_changed)

    return device

# 处理JS中不同的信息
def deal_message(payload):
    # 基本信息输出
    if payload.has_key('mes'):
        print( payload['mes'])

        # 安装app信息
    if payload.has_key('app'):
        app = payload['app']
        lines = app.split('\n')
        for line in lines:
            if len(line):
                arr = line.split('\t')
                if len(arr) == 3:
                    outWrite('%-40s\t%-70s\t%-80s' % (arr[0], arr[1], arr[2]))

                    # 处理UI界面输出
    if payload.has_key('ui'):
        print (colorPrint(31, payload['ui']))

        # 处理完成事件
    if payload.has_key('finished'):
        finished.set()

# 从JS接受信息
def on_message(message, data):
    print (message)
    if 'payload' in  message:
        payload = message['payload']
        if isinstance(payload, dict):  # 如果是字典
            deal_message(payload)
        else:
            print (payload)

# 加载JS文件脚本
def loadJsFile(session, filename):
    source = ''
    # with codecs.open(filename, 'r', 'utf-8') as f:
    #     source = source + f.read()
    with open(filename, 'r') as f:
        source = source + f.read()
    script = session.create_script(source)  # 加载脚本
    script.on('message', on_message)
    script.load()
    return script


appname = 'something'

def main():
    global session
    # 1. 获取USB设备
    device = {}
    device = get_usb_iphone()
    print ('设备信息:' + str(device))

    # 6. 动态Hook
    session = {}
    try:
        session = device.attach(appname)
        print('try session',session)
    except Exception as e:
        print('Exception',e)
        while session == {}:
            try:
                session = device.attach(appname) 
            except frida.ProcessNotFoundError:
                pass
        print('except session',session)

    
    while session == {}:
        try:
            session = device.attach(appname) 
        except frida.ProcessNotFoundError:
            pass
            # print(session)
    script = loadJsFile(session, './js/hook_DANA.js')
    sys.stdin.read()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if session:
            session.detach()
        sys.exit()
    else:
        pass
    finally:
        pass

