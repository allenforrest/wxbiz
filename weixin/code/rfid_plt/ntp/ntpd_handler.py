#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTPD NTP�������õ�Handler��Handler��������NTPD�������ã��򿪹ر�NTP���񣬻�ȡNTPD�������õ���Ϣ
Others:    ��
Key Class&Method List: 
             1. NtpdServerControlHandler��handler�࣬����򿪹ر�NTPD����
             2. AddSubnetHandler�� handler�࣬����ΪNTPD����������
             3. AddServerHandler�� handler�࣬����ΪNTPD���÷�����IP��ַ
             4. GetSubnetHandler�� handler�࣬�����ȡNTPD��������
             5. GetServerHandler�� handler�࣬�����ȡNTPD��IP��ַ
             6. DelSubnetHandler�� handler�࣬����ɾ��NTPD��ĳ��������
             7. DelServerHandler�� handler�࣬����ɾ��NTPD��ĳ��������IP��ַ
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:�½��ļ�
"""


import bundleframework as bf
import tracelog
import err_code_mgr

import ntpd_params
import ntpd_set

class NtpdServerControlHandler(bf.CmdHandler):
    """
    Class: NtpdServerControlHandler
    Description: �򿪹ر�NTPD����
    Base: CmdHandler
    Others: 1. ���ز���Ϊon,off
            2. �򿪷���ʱ��stratum��ЧֵΪ1-15������ԽС�����ȼ�Խ��
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: �򿪹ر�NTPD����
        Parameter: 
            frame: �յ��Ĵ�����Ϣ
            data��1��������
            msg��NtpdControl����
        Return: ��
        Others: 1. ���ز���Ϊon,off
                2. �򿪷���ʱ��stratum��ЧֵΪ1-15����ֵԽС�����ȼ�Խ��
        """

        try:
            msg = ntpd_params.NtpdControl().deserialize(frame.get_data())
        except:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
        
        rdms = self.get_worker().get_mit_manager().rdm_find("NtpdControlMOC")
        if len(rdms)==0:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_DB_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_DB_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
            
        if rdms[0].openserver==msg.openserver:
            response= ntpd_params.GetNtpdHandlerResult() 
            response.return_code = err_code_mgr.ER_NTPD_HAS_OP_ERROR
            response.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_HAS_OP_ERROR)
            self.get_worker().send_ack(frame, (response.serialize(), ))
            return

        rdms[0].openserver = msg.openserver
        rdms[0].stratum = msg.stratum
        ret = self.get_worker().get_mit_manager().rdm_mod(rdms[0])
        if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
            result = ntpd_params.GetNtpdHandlerResult() 
            result.init_all_attr()
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return

        return_code, description = ntpd_set.ntpd_write(self.get_worker().get_mit_manager()) 
        response= ntpd_params.GetNtpdHandlerResult()    
        response.return_code = return_code
        response.description = description
        self.get_worker().send_ack(frame, (response.serialize(), ))    
              
class AddSubnetHandler(bf.CmdHandler):
    """
    Class: AddSubnetHandler
    Description: ΪNTPD��������������
    Base: CmdHandler
    Others: ��
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ΪNTPD��������������
        Parameter: 
            frame: �յ��Ĵ�����Ϣ
            data��һ��������
            msg��NtpdSubnet����
        Return: ��
        Others: ��
        """

        try:
            msg = ntpd_params.NtpdSubnet().deserialize(frame.get_data())
        except:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
        
        if msg.subnetip is None or msg.mask is None:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return

        ntpdsubnet_moc = self.get_worker().get_mit_manager().gen_rdm("NtpdSubnetMOC")        
        ntpdsubnet_moc.subnetip = msg.subnetip
        ntpdsubnet_moc.mask = msg.mask  
        ret = self.get_worker().get_mit_manager().rdm_add(ntpdsubnet_moc)
        
        if ret.get_err_code()==err_code_mgr.ER_OBJECT_ADD_CONFLICT:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_DUPLICATE_NTPD_SUBNET_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_DUPLICATE_NTPD_SUBNET_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
        if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
 
        return_code, description = ntpd_set.ntpd_write(self.get_worker().get_mit_manager()) 
        response= ntpd_params.GetNtpdHandlerResult()    
        response.return_code = return_code
        response.description = description
        self.get_worker().send_ack(frame, (response.serialize(), ))  
        
class AddServerHandler(bf.CmdHandler):
    """
    Class: AddServerHandler
    Description: ΪNTPD���÷�����IP��ַ
    Base: CmdHandler
    Others: ��
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ΪNTPD���÷�����IP��ַ
        Parameter: 
            frame: �յ��Ĵ�����Ϣ
            data��һ������
            msg��NtpdServer����
        Return: ��
        Others: ��
        """

        try:
            msg = ntpd_params.NtpdServer().deserialize(frame.get_data())
        except:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
        
        if msg.serverip is None:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
            
        ntpdserver_moc = self.get_worker().get_mit_manager().gen_rdm("NtpdServerMOC")        
        ntpdserver_moc.serverip = msg.serverip     
        ret = self.get_worker().get_mit_manager().rdm_add(ntpdserver_moc)
        
        if ret.get_err_code()==err_code_mgr.ER_OBJECT_ADD_CONFLICT:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_DUPLICATE_NTPD_SERVER_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_DUPLICATE_NTPD_SERVER_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
        if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
              
        return_code, description = ntpd_set.ntpd_write(self.get_worker().get_mit_manager()) 
        response= ntpd_params.GetNtpdHandlerResult()    
        response.return_code = return_code
        response.description = description 
        self.get_worker().send_ack(frame, (response.serialize(), ))   
        
class GetSubnetHandler(bf.CmdHandler):
    """
    Class: GetSubnetHandler
    Description: ��ȡNTPD��������
    Base: CmdHandler
    Others: ��
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ��ȡNTPD��������
        Parameter: 
            frame: �յ��Ĵ�����Ϣ
        Return: ��
        Others: ��
        """

        records = self.get_worker().get_mit_manager().lookup_attrs("NtpdSubnetMOC", ['subnetip', 'mask'])
   
        results = ntpd_params.GetNtpdSubnetListResult()
        results.init_all_attr()
        results.ntpdsubnets = []  
        
        for record in records:
            ntpdsubnet = ntpd_params.NtpdSubnet()
            ntpdsubnet.init_all_attr()
            ntpdsubnet.subnetip = record[0]
            ntpdsubnet.mask= record[1]
            results.ntpdsubnets.append(ntpdsubnet)
        
        results.return_code = err_code_mgr.ER_SUCCESS
        results.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        self.get_worker().send_ack(frame, (results.serialize(), ))
        
class GetServerHandler(bf.CmdHandler):
    """
    Class: GetServerHandler
    Description: ��ȡNTPD������IP��ַ
    Base: CmdHandler
    Others: ��
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ��ȡNTPD������IP��ַ
        Parameter: 
            frame: �յ��Ĵ�����Ϣ
        Return: ��
        Others: ��
        """

        records = self.get_worker().get_mit_manager().lookup_attrs("NtpdServerMOC", ['serverip'])
    
        results = ntpd_params.GetNtpdServerListResult()
        results.init_all_attr()
        results.ntpdservers = []  
        
        for record in records:
            ntpdserver = ntpd_params.NtpdServer()
            ntpdserver .init_all_attr()
            ntpdserver .serverip = record[0]
            results.ntpdservers.append(ntpdserver)
        
        results.return_code = err_code_mgr.ER_SUCCESS
        results.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        self.get_worker().send_ack(frame, (results.serialize(), ))
        
class DelSubnetHandler(bf.CmdHandler):
    """
    Class: DelSubnetHandler
    Description: ɾ��NTPD��ĳ��������
    Base: CmdHandler
    Others: ��
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ɾ��NTPD��ĳ��������
        Parameter: 
            frame: �յ��Ĵ�����Ϣ
            data��һ��������
            msg��NtpdSubnet����
        Return: ��
        Others: ��
        """

        try:
            msg = ntpd_params.NtpdSubnet().deserialize(frame.get_data())
        except:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
        
        if msg.subnetip is None or msg.mask is None:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return

        ntpdsubnet_moc = self.get_worker().get_mit_manager().gen_rdm("NtpdSubnetMOC")  
        ntpdsubnet_moc.subnetip = msg.subnetip
        ntpdsubnet_moc.mask = msg.mask
           
        ret = self.get_worker().get_mit_manager().rdm_remove(ntpdsubnet_moc)
        if ret.get_err_code() == err_code_mgr.ER_OBJECT_NOT_EXIST:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_SUBNET_NOT_EXIST
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_SUBNET_NOT_EXIST)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
        if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return

        return_code, description = ntpd_set.ntpd_write(self.get_worker().get_mit_manager()) 
        response= ntpd_params.GetNtpdHandlerResult()    
        response.return_code = return_code
        response.description = description 
        self.get_worker().send_ack(frame, (response.serialize(), ))   
        
class DelServerHandler(bf.CmdHandler):
    """
    Class: DelServerHandler
    Description: ɾ��NTPD��ĳ��������IP��ַ
    Base: CmdHandler
    Others: ��
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ɾ��NTPD��ĳ��������IP��ַ
        Parameter: 
            frame: �յ��Ĵ�����Ϣ
            data��һ������
            msg��NtpdServer����
        Return: ��
        Others: ��
        """

        try:
            msg = ntpd_params.NtpdServer().deserialize(frame.get_data())
        except:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
        
        if msg.serverip is None:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_INVALID_DESERIALIZE_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return
        
        ntpdserver_moc = self.get_worker().get_mit_manager().gen_rdm("NtpdServerMOC")  
        ntpdserver_moc.serverip = msg.serverip
           
        ret = self.get_worker().get_mit_manager().rdm_remove(ntpdserver_moc)
        if ret.get_err_code() == err_code_mgr.ER_OBJECT_NOT_EXIST:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = err_code_mgr.ER_NTPD_SERVER_NOT_EXIST
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_SERVER_NOT_EXIST)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return 
        if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
            result = ntpd_params.GetNtpdHandlerResult()
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return   

        return_code, description = ntpd_set.ntpd_write(self.get_worker().get_mit_manager()) 
        response= ntpd_params.GetNtpdHandlerResult()    
        response.return_code = return_code
        response.description = description    
        self.get_worker().send_ack(frame, (response.serialize(), ))
        