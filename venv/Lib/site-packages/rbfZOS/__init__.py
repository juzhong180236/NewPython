# -*- encoding: utf-8 -*-

#  Copyright 2019-  DNB
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from rbfZOS.x3270 import x3270



__version__ = "1.0"


class rbfZOS(x3270):
    """rbfZOS is a library for Robot Framework based on [https://pypi.org/project/py3270/|py3270 project],
       a Python interface to x3270, an IBM 3270 terminal emulator. It provides an API to a x3270 or s3270 subprocess.
       = Installation  =
       
       For use this library you need to install the [http://x3270.bgp.nu/download.html|x3270 project]
       and put the directory on your PATH. On Windows, you need to download wc3270 and put
       the "C:\Program Files\wc3270" in PATH of the Environment Variables.
              
       = Notes  =
       By default the import set the visible argument to true, on this option the py3270 is running the wc3270.exe,
       but is you set the visible to false, the py3270 will run the ws3270.exe.
             
       
       
       = Mainframe Example =
       | ***** Settings *****
       | Library           rbfZOS
       | Library           BuiltIn
       |
       | ***** Test Cases *****
       | Example
       |     Open Connection    Hostname    LUname
       |     Change Wait Time    0.9
       |     Set Screenshot Folder    C:\\\Temp\\\IMG
       |     ${value}    Read    3    10    17
       |     Page Should Contain String    ENTER APPLICATION
       |     Write Bare    applicationname
       |     Send Enter
       |     Take Screenshot
       |     Close Connection 
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__
