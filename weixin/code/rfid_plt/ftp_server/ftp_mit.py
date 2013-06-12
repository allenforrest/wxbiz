#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: 负责注册ftp_server的mit
Others: 无 
Key Class&Method List: 
             1. FtpServerMit: 负责注册ftp_server的mit
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:新建文件
"""

import mit
from dba import db_cfg_info


import FtpServerUserMOC
import FtpServerAcceptorMOC
import FtpServerCtrlLinkMOC
import FtpServerDataLinkMOC
import FtpServerFTPSMOC
import FtpServerMasqueradeAddr
import FtpServerPortMOC

class FtpServerMit(mit.Mit):
    """
    Class: FtpServerMit
    Description: 负责注册ftp_server的mit
    Base: Mit
    Others: 无
    """
    def __init__(self):
        """
        Method: __init__
        Description: 初始化
        Parameter: 无
        Return: 无
        Others: 无
        """
        mit.Mit.__init__(self)
        self.regist_moc(FtpServerUserMOC.FtpServerUserMOC, FtpServerUserMOC.FtpServerUserMOCRule)
        self.regist_moc(FtpServerAcceptorMOC.FtpServerAcceptorMOC, FtpServerAcceptorMOC.FtpServerAcceptorMOCRule)
        self.regist_moc(FtpServerCtrlLinkMOC.FtpServerCtrlLinkMOC
                                     , FtpServerCtrlLinkMOC.FtpServerCtrlLinkMOCRule)
        self.regist_moc(FtpServerDataLinkMOC.FtpServerDataLinkMOC
                                     , FtpServerDataLinkMOC.FtpServerDataLinkMOCRule)
        self.regist_moc(FtpServerFTPSMOC.FtpServerFTPSMOC, FtpServerFTPSMOC.FtpServerFTPSMOCRule)
        self.regist_moc(FtpServerMasqueradeAddr.FtpServerMasqueradeAddr
                                     , FtpServerMasqueradeAddr.FtpServerMasqueradeAddrRule)
        self.regist_moc(FtpServerPortMOC.FtpServerPortMOC
                                     , FtpServerPortMOC.FtpServerPortMOCRule)
                                     
        self.open_sqlite("./ftp_server.db")
        #self.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME))
        