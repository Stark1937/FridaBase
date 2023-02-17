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

Date         : 2023-02-16 16:04:54
LastEditors  : Stark1937
LastEditTime : 2023-02-16 16:31:50
FilePath     : /FridaBase/refelaction.py
'''

import frida, sys

f = open('./tmp/log', 'w')    

def on_message(msg, _data):
    f.write(msg['payload']+'\n')

frida_script = """
  Interceptor.attach(Module.findExportByName('/usr/lib/libobjc.A.dylib', 'objc_msgSend'), {
    onEnter: function(args) {
     var m = Memory.readCString(args[1]);
     # if (m != 'length' && !m.startsWith('_fastC'))
     if (m != 'length' || !m.startsWith('_fastC' || m != 'retain' || m != 'release'))
        send(m);
    }
  });
"""
device = frida.get_usb_device()
# pid = device.spawn(["com.telkomsel.wallet"]) # or .get_frontmost_application()
pid = device.get_frontmost_application().pid
session = device.attach(pid)
script = session.create_script(frida_script)
script.on('message', on_message)
script.load()
device.resume(pid)
sys.stdin.read()