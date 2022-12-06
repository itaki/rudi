import threading
from sshkeyboard import listen_keyboard

def press(key):
    print(f"'{key}' pressed")

def release(key):
    print(f"'{key}' released")

def doThing():
    listen_keyboard(
        on_press=press,
        on_release=release,
    )

# creating new thread
t1 = threading.Thread(target=doThing)

# starting new thread
t1.start()

print("do more stuff")

while True:
    pass
