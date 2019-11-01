# BatchInstall.py
import os

try:
    os.system('''pyinstaller -F exec_ws.py''')
    print("Successful")
except:
    print("Failed Somehow")
