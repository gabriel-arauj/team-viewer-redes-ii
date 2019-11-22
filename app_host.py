from rdt_sender import Sender
from rdt_receiver import Receiver
import pyautogui
import time
from PIL import Image
from multiprocessing import Process
from pynput.keyboard import Key, Listener, Controller




my_address = ('127.0.0.1', 40001)
other_address = ('127.0.0.1', 40000)
def view():
    S = Sender(other_address)
    while True:
        im = pyautogui.screenshot()
        im = im.resize((800,600),Image.ANTIALIAS)
        data = im.tobytes().decode('ANSI')
        S.rdt_send(data)
    S.close()

def keyboard():
    key_map = {
        "'a'": 'a',
        "'b'": 'b',
        "'c'": 'c',
        "'d'": 'd',
        "'e'": 'e',
        "'f'": 'f',
        "'g'": 'g',
        "'h'": 'h',
        "'i'": 'i',
        "'j'": 'j',
        "'k'": 'k',
        "'l'": 'l',
        "'m'": 'm',
        "'n'": 'n',
        "'o'": 'o',
        "'p'": 'p',
        "'q'": 'q',
        "'r'": 'r',
        "'s'": 's',
        "'t'": 't',
        "'u'": 'u',
        "'v'": 'v',
        "'w'": 'w',
        "'x'": 'x',
        "'y'": 'y',
        "'z'": 'z',
        "'1'": '1',
        "'2'": '2',
        "'3'": '3',
        "'4'": '4',
        "'5'": '5',
        "'6'": '6',
        "'7'": '7',
        "'8'": '8',
        "'9'": '9',
        "'0'": '0',
        "'-'": '-',
        "'='": '=',
        "'['": '[',
        "']'": ']',
        "';'": ';',
        "'/'": '/',
        "'.'": '.',
        "','": ',',
        "'*'": '*',
        "'\\\\'":'\\',
        'Key.alt': Key.alt,
        'Key.alt_l': Key.alt_l,
        'Key.alt_r': Key.alt_r,
        'Key.alt_gr': Key.alt_gr,
        'Key.backspace': Key.backspace,
        'Key.caps_lock': Key.caps_lock,
        'Key.cmd': Key.cmd,
        'Key.cmd_l': Key.cmd_l,
        'Key.cmd_r': Key.cmd_r,
        'Key.ctrl': Key.ctrl,
        'Key.ctrl_l': Key.ctrl_l,
        'Key.ctrl_r': Key.ctrl_r,
        'Key.delete': Key.delete,
        'Key.down': Key.down,
        'Key.end': Key.end,
        'Key.enter': Key.enter,
        'Key.esc': Key.esc,
        'Key.f1': Key.f1,
        'Key.f2': Key.f2,
        'Key.f3': Key.f3,
        'Key.f4': Key.f4,
        'Key.f5': Key.f5,
        'Key.f6': Key.f6,
        'Key.f7': Key.f7,
        'Key.f8': Key.f8,
        'Key.f9': Key.f9,
        'Key.f10': Key.f10,
        'Key.f11': Key.f11,
        'Key.f12': Key.f12,
        'Key.f13': Key.f13,
        'Key.f14': Key.f14,
        'Key.f15': Key.f15,
        'Key.f16': Key.f16,
        'Key.f17': Key.f17,
        'Key.f18': Key.f18,
        'Key.f19': Key.f19,
        'Key.f20': Key.f20,
        'Key.home': Key.home,
        'Key.left': Key.left,
        'Key.page_down': Key.page_down,
        'Key.page_up': Key.page_up,
        'Key.right': Key.right,
        'Key.shift': Key.shift,
        'Key.shift_l': Key.shift_l,
        'Key.shift_r': Key.shift_r,
        'Key.space': Key.space,
        'Key.tab': Key.tab,
        'Key.up': Key.up,
        'Key.insert': Key.insert,
        'Key.menu': Key.menu,
        'Key.num_lock': Key.num_lock,
        'Key.pause': Key.pause,
        'Key.print_screen': Key.print_screen,
        'Key.scroll_lock': Key.scroll_lock
    }
    R = Receiver(my_address)
    while True:
        action, key = R.rdt_recv().split(':')
        keyboard = Controller()
        if action == "press":
            try:
                keyboard.press(key_map[str(key)])
            except KeyError:
                print("Caracter desconhecido")
        else:
            try:
                keyboard.release(key_map[str(key)])
            except KeyError:
                print("Caracter desconhecido")
        if key == 'Key.esc':
            return


if __name__ == "__main__": 
    # creating processes 
    p1 = Process(target=view) 
    p2 = Process(target=keyboard) 
  
    # starting process 1 
    p1.start() 
    # starting process 2 
    p2.start() 
  
    # wait until process 1 is finished 
    p1.join() 
    # wait until process 2 is finished 
    p2.join() 
  
    # both processes finished 
    print("Done!") 
