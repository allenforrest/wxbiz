#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: ����ע��ftp_server��mit
Others: �� 
Key Class&Method List: 
             1. FtpServerMit: ����ע��ftp_server��mit
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:�½��ļ�
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
    Description: ����ע��ftp_server��mit
    Base: Mit
    Others: ��
    """
    def __init__(self):
        """
        Method: __init__
        Description: ��ʼ��
        Parameter: ��
        Return: ��
        Others: ��
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
        