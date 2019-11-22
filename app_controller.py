from rdt_receiver import Receiver
from rdt_sender import Sender
from PIL import Image, ImageTk
import tkinter as tk
import time
from multiprocessing import Process
from pynput.keyboard import Key, Listener, Controller

my_address = ('127.0.0.1', 40000)
host_address = ('127.0.0.1', 40001)

def view():
    R = Receiver(my_address)
    def get_image():
        data = R.rdt_recv()
        im = Image.frombytes("RGB", (800 , 600), data.encode('ANSI'))
        return im


    def callback():
        img2 = ImageTk.PhotoImage(get_image())
        panel.configure(image=img2)
        panel.image = img2
        root.update_idletasks()
        root.after(400, callback)


    root = tk.Tk()
    img = ImageTk.PhotoImage(get_image())
    panel = tk.Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    callback()
    root.mainloop()

def keyboard():
    S = Sender(host_address)

    def on_press(key):
        print('{0} pressed'.format(
            key))
        S.rdt_send("press:" + str(key))

    def on_release(key):
        print('{0} release'.format(
            key))
        S.rdt_send("release:" + str(key))
        if key == Key.esc:
            # Stop listener
            return False

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


        

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
