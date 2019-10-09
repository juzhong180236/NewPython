# Copyright 2019-     DNB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from .rbfFTP import rbfFTP
from .version import __version__



class rbfFTP(rbfFTP):
    """rbfFTP is a ftp client library for Robot Framework.

    This library provides functionality of FTP client.


The simplest example (connect, change working dir, print working dir, close):
 | ftp connect | 192.168.1.10 | mylogin | mypassword |
 | cwd | /home/myname/tmp/testdir |
 | pwd |
 | ftp close |

It is possible to use multiple ftp connections in parallel. Connections are
identified by string identifiers:
 | ftp connect | 192.168.1.10 | mylogin | mypassword | connId=ftp1 |
 | ftp connect | 192.168.1.20 | mylogin2 | mypassword2 | connId=ftp2 |
 | cwd | /home/myname/tmp/testdir | ftp1 |
 | cwd | /home/myname/tmp/testdir | ftp2 |
 | pwd | ftp2 |
 | pwd | ftp1 |
 | ftp close | ftp2 |
 | ftp close | ftp1 |

To run library remotely execute: python rbfFTP.py <ipaddress> <portnumber>
(for example: python rbfFTP.py 192.168.0.101 8222)
    
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = __version__
