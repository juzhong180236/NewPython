# BatchInstall.py
import os

try:
    os.system('''cd /d C:/Users/asus/Desktop/DT_DEMO/ws & \
                pkg -t win ws.js
              ''')
    print("Successful")
except:
    print("Failed Somehow")
