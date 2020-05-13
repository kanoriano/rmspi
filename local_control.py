import socket
import sys
import time
from pynput.keyboard import Key, Listener

leftM=0
rightM=0
servo4=90
servo5=90

print("Key control: Left motor '+left shift' '-left ctrl'")
print("             Right motor '+right shift' '-right ctrl'")
print("             Horizontal alt_left/alt_right keys")
print("             Vertical page up/page down")
print("             Space to reset 0 platform motors")
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 7001)
sock.connect(server_address)

def on_press(key):
    print('{0} pressed'.format(key))
    global leftM
    global rightM
    global servo4
    global servo5
    if key == Key.shift:
        leftM=leftM+100
        #if leftM < 1000:
            #leftM=leftM+1000
        sock.sendall(("0<{0}".format(leftM)).encode())
    if key == Key.space:
        leftM=0
        rightM=0
        sock.sendall(("0<{0}".format(leftM)).encode())
        sock.sendall(("1<{0}".format(rightM)).encode())
    if key == Key.shift_r:
        rightM=rightM+100
        #if rightM < 1000:
            #rightM=rightM+1000
                        sock.sendall(("1<{0}".format(rightM)).encode())
    if key == Key.ctrl_l:
        leftM=leftM-100
        sock.sendall(("0<{0}".format(leftM)).encode())
    if key == Key.ctrl_r:
        rightM=rightM-100
        sock.sendall(("1<{0}".format(rightM)).encode())
    if key == Key.alt_l:
        servo4=servo4+1
        if servo4 > 180:
            servo4=servo4-1
        sock.sendall(("4<{0}".format(servo4)).encode())
    if key == Key.alt_r:
        servo4=servo4-1
        if servo4 < 0:
            servo4=servo4+1
        sock.sendall(("4<{0}".format(servo4)).encode())
    if key == Key.page_up:
        servo5=servo5+1
        if servo5 > 180:
            servo5=servo5-1
        sock.sendall(("5<{0}".format(servo5)).encode())
    if key == Key.page_down:
        servo5=servo5-1
        if servo5 < 0:
            servo5=servo5+1
        sock.sendall(("5<{0}".format(servo5)).encode())
    if key == Key.enter:
        leftM=1500
        rightM=1500
        sock.sendall(("0<{0}".format(leftM)).encode())
        sock.sendall(("1<{0}".format(rightM)).encode())
        
    print("Left motor %s Right motor %s Horizont %s Vertical %s" % (leftM, rightM, servo4, servo5))

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
# Send data

sock.sendall('exit'.encode())
time.sleep(1)
sock.close()
