# -*- coding: utf-8 -*-

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

import ftplib
import os
import socket
from robot.api import logger
from robot.api.deco import keyword

class rbfFTP(object):

    """
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

    def __getConnection(self, connId):
        if connId in self.ftpList:
            return self.ftpList[connId]
        else:
            errMsg = "Connection with ID %s does not exist. It should be created before this step." % connId
            raise rbfFTPError(errMsg)

    def __addNewConnection(self, connObj, connId):
        if connId in self.ftpList:
            errMsg = "Connection with ID %s already exist. It should be deleted before this step." % connId
            raise rbfFTPError(errMsg)
        else:
            self.ftpList[connId] = connObj

    def __removeConnection(self, connId):
        if connId in self.ftpList:
            self.ftpList.pop(connId)

    @keyword
    def getAllFtpConnections(self):
        """
        *Returns a dictionary containing active ftp connections.*
        """
        outputMsg = "Current ftp connections:\n"
        counter = 1
        for k in self.ftpList:
            outputMsg += str(counter) + ". " + k + " "
            outputMsg += str(self.ftpList[k]) + "\n"
            counter += 1
        if self.printOutput:
            logger.info(outputMsg)
        return self.ftpList

    @keyword
    def ftp_connect(self, host, user='anonymous', password='anonymous@', port=21, timeout=30, connId='default'):
        """
        *Constructs FTP object, opens a connection and login. Returns server output.*
        Call this function before any other (otherwise raises exception).
        
        
        *Arguments*
        
            ``host``: server host address
            
            ``user``: Optional. FTP user name. If not given, 'anonymous' is used.
            
            ``password``: Optional. FTP password. If not given, 'anonymous@' is used.
            
            ``port``: Optional. TCP port. By default 21.
            
            ``timeout``: Optional. Timeout in seconds. By default 30.
            
            ``connId``: Optional. Connection identifier. By default equals 'default'
            
        *Examples*
        
        | `ftp connect` | 192.168.1.10 | mylogin | mypassword |  |  |
        | `ftp connect` | 192.168.1.10 |  |  |  |  |
        | `ftp connect` | 192.168.1.10 | mylogin | mypassword | connId=secondConn |  |
        | `ftp connect` | 192.168.1.10 | mylogin | mypassword | 29 | 20 |
        | `ftp connect` | 192.168.1.10 | mylogin | mypassword | 29 |  |
        | `ftp connect` | 192.168.1.10 | mylogin | mypassword | timeout=20 |  |
        | `ftp connect` | 192.168.1.10 | port=29 | timeout=20 |  |  |
        """
        if connId in self.ftpList:
            errMsg = "Connection with ID %s already exist. It should be deleted before this step." % connId
            raise rbfFTPError(errMsg)
        else:
            newFtp = None
            outputMsg = ""
            try:
                timeout = int(timeout)
                port = int(port)
                newFtp = ftplib.FTP()
                outputMsg += newFtp.connect(host, port, timeout)
                outputMsg += newFtp.login(user,password)
            except socket.error as se:
                raise rbfFTPError('Socket error exception occured.')
            except ftplib.all_errors as e:
                raise rbfFTPError(str(e))
            except Exception as e:
                raise rbfFTPError(str(e))
            if self.printOutput:
                logger.info(outputMsg)
            self.__addNewConnection(newFtp, connId)

    @keyword
    def get_welcome(self, connId='default'):
        """
        *Returns wlecome message of FTP server.*
        
        *Arguments*
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
            
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += thisConn.getwelcome()
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    
    @keyword
    def pwd(self, connId='default'):
        """
        *Returns the pathname of the current directory on the server.*
        
        *Arguments*
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += thisConn.pwd()
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    
    @keyword
    def cwd(self, directory, connId='default'):
        """
        *Changes working directory and returns server output.* 
        
        *Arguments*
        
        ``directory``: A path to which working dir should be changed.
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
        
        *Examples*
        
        | `cwd` | /home/myname/tmp/testdir |  |
        | `cwd` | /home/myname/tmp/testdir | ftp1 |
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += thisConn.cwd(directory)
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    @keyword
    def dir(self, connId='default'):
        """
        *Returns list of raw lines returned as contens of current directory.*
        
        *Arguments*
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
        """
        dirList = []
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            thisConn.dir(dirList.append)
            for d in dirList:
                outputMsg += str(d) + "\n"
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return dirList

    
    @keyword
    def dir_names(self, connId='default'):
        """
        *Returns list of files (and/or directories) of current directory.*
        
        *Arguments*
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
        """
        files_list = []
        thisConn = self.__getConnection(connId)
        try:
            files_list = thisConn.nlst()
        except:
            files_list = []
        return files_list

    
    @keyword
    def mkd(self, newDirName, connId='default'):
        """
        *Creates new directory on FTP server. Returns new directory path.*
        
        *Arguments*
        
        ``newDirName``: Name of new directory
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
        
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += str(thisConn.mkd(newDirName))
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    
    @keyword
    def rmd(self, directory, connId='default'):
        """
        *Deletes directory from FTP server. Returns server output.*
        
        *Arguments*
        
        ``directory``: Path to a directory to be deleted
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
        
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += str(thisConn.rmd(directory))
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    
    @keyword
    def download_file(self, remoteFileName, localFilePath=None, connId='default'):
        """
        *Downloads file from current directory on FTP server in binary mode. Returns server output.*
        If localFilePath is not given, file is saved in current local directory (by
        default folder containing robot framework project file) with the same name
        as source file. 
        
        *Arguments*
        
        ``remoteFileName``: File name on FTP server
        
        ``localFilePath``: Optional. Local file name or path where remote file should be saved. localFilePath variable can have following meanings:
        - file name (will be saved in current default directory);
        - full path (dir + file name)
        - dir path (original file name will be added)
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
                
        *Examples*
        
        | `download file` | a.txt |  |  |
        | `download file` | a.txt | b.txt | connId=ftp1 |
        | `download file` | a.txt | D:/rfftppy/tmp |  |
        | `download file` | a.txt | D:/rfftppy/tmp/b.txt |  |
        | `download file` | a.txt | D:\\rfftppy\\tmp\\c.txt |  |
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        localPath = ""
        if localFilePath == None:
            localPath = remoteFileName
        else:
            localPath = os.path.normpath(localFilePath)
            if os.path.isdir(localPath):
                localPath = os.path.join(localPath, remoteFileName)
        try:
            with open(localPath, 'wb') as localFile:
                outputMsg += thisConn.retrbinary("RETR " + remoteFileName, localFile.write)
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    
    @keyword
    def upload_file(self, localFileName, remoteFileName=None, connId='default'):
        """
        *Sends file from local drive to current directory on FTP server in binary mode. Returns server output.*
        
        
        *Arguments*
        
        ``localFileName``: File name or path to a file on a local drive.
        
        ``remoteFileName``: Optional. A name or path containing name under which file should be saved.
        If remoteFileName agument is not given, local name will be used.
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
       
        *Examples*
        
        | `upload file` | x.txt | connId=ftp1 |
        | `upload file` | D:/rfftppy/y.txt |  |
        | `upload file` | u.txt | uu.txt |
        | `upload file` | D:/rfftppy/z.txt | zz.txt |
        | `upload file` | D:\\rfftppy\\v.txt |  |
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        remoteFileName_ = ""
        localFilePath = os.path.normpath(localFileName)
        if not os.path.isfile(localFilePath):
            raise rbfFTPError("Valid file path should be provided.")
        else:
            if remoteFileName==None:
                fileTuple = os.path.split(localFileName)
                if len(fileTuple)==2:
                    remoteFileName_ = fileTuple[1]
                else:
                    remoteFileName_ = 'defaultFileName'
            else:
                remoteFileName_ = remoteFileName
            try:
                outputMsg += thisConn.storbinary("STOR " + remoteFileName_, open(localFilePath, "rb"))
            except ftplib.all_errors as e:
               raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    
    @keyword
    def size(self, fileToCheck, connId='default'):
        """
        *Checks size of a file on FTP server. Returns size of a file in bytes (integer).*
        Note that the SIZE command is not standardized, but is supported by many common server implementations.
        
        *Arguments*
        
        ``fileToCheck``: File name or path to a file on FTP server
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
        
        *Examples*
        
        | ${file1size} = | `size` | /home/myname/tmp/uu.txt | connId=ftp1 |
        | Should Be Equal As Numbers | ${file1size} | 31 |  |

        
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            tmpSize = thisConn.size(fileToCheck)
            outputMsg += str(tmpSize)
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    
    @keyword
    def rename(self, targetFile, newName, connId='default'):
        """
        *Renames (actually moves) file on FTP server. Returns server output.*
        
        
        *Arguments*
        
        ``targetFile``: Name of a file or path to a file to be renamed
        
        ``newName``: New name or new path
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
        
        *Arguments*
        
        | `rename` | tmp/z.txt | /home/myname/tmp/testdir/z.txt |
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += str(thisConn.rename(targetFile, newName))
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    
    @keyword
    def delete(self, targetFile, connId='default'):
        """
        *Deletes file on FTP server. Returns server output.*
        
        *Arguments*
        
        ``targetFile``: Name of a file or path to a file to be renamed
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += str(thisConn.delete(targetFile))
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    
    @keyword
    def send_cmd(self, command, connId='default'):
        """
        *Sends any command to FTP server. Returns server output.*
        
        *Arguments*
        
        ``command``: Any valid command to be sent (invalid will result in exception).
        
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
        *Examples*
        
        | `send cmd` | HELP |
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += str(thisConn.sendcmd(command))
        except ftplib.all_errors as e:
            raise rbfFTPError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    
    @keyword
    def ftp_close(self, connId='default'):
        """
        *Closes FTP connection. Returns None.*
        
        *Arguments*
              
        ``connId``: Optional. Connection identifier. By default equals 'default'
        
        """
        thisConn = self.__getConnection(connId)
        try:
            thisConn.quit()
            self.__removeConnection(connId)
        except Exception as e:
            try:
                thisConn.close()
                self.__removeConnection(connId)
            except ftplib.all_errors as x:
                raise rbfFTPError(str(x))

    def __del__(self):
        self.ftpList = {}

class rbfFTPError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def main():
    import sys
    from robotremoteserver import RobotRemoteServer
    print("Starting Robot Framework Ftp Library as a remote server ...")
    RobotRemoteServer(library=rbfFTP(), host=sys.argv[1], port=sys.argv[2])

if __name__ == '__main__':
    main()
