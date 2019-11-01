# BatchInstall.py
import os

try:
    os.system('''cd /d C:/Users/asus/Desktop/DT_DEMO/ws & \
                pkg -t win ws.js        
              ''')
    os.system('''cd /d C:/Users/asus/Desktop/DT_DEMO/ws & \
                pkg package.json
                  ''')
    print("Successful")
except:
    print("Failed Somehow")
