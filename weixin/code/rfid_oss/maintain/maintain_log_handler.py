#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: maintain log�Ķ�ʱά����log�����ڴ����log������������ѯ
Others:��
Key Class&Method List: 
             1. PackageLogHandler��������־���
             2. PackageLogExportTaskQueryHandler�� ���������������ѯ
             3. ZipLogFileTimeoutHandler�� ���ڽ���ת����־ѹ������
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:�½��ļ�
"""



import bundleframework as bf
import tracelog
import err_code_mgr

import maintain_log_params


class PackageLogHandler(bf.CmdHandler):    
    """
    Class: PackageLogHandler
    Description: ��־���
    Base: CmdHandler
    Others: ��
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ��־���
        Parameter: 
            frame: �յ��Ĵ�����Ϣ
            data��1��������
            msg��PackageLog����
        Return: ��
        Others: ��
        """

        try:
            req = maintain_log_params.PackageLog().deserialize(frame.get_data())
        except Exception:
            result = maintain_log_params.PackageLogHandlerResult()
            result.init_all_attr()           
            result.user_session = ''
            result.return_code = err_code_mgr.ER_MAINTAINLOG_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_MAINTAINLOG_INVALID_DESERIALIZE_ERROR
                                                            ,cmd = 'PackageLogHandler')
            result.task_no = 0            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return
            
        result = self.get_worker().get_maintain_log_manager().new_task(req)
                                    
        self.get_worker().get_app().send_ack(frame, (result.serialize(), ))
        
class PackageLogExportTaskQueryHandler(bf.CmdHandler):
    """
    Class: PackageLogExportTaskQueryHandler
    Description: ������������ѯ
    Base: CmdHandler
    Others: ��
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ������������ѯ
        Parameter: 
            frame: �յ��Ĵ�����Ϣ
            data��1��������
            msg��PackageLogExportTaskRequest���� 
        Return: ��
        Others: ��
        """

        try:
            req = maintain_log_params.PackageLogExportTaskRequest().deserialize(frame.get_data())
        except Exception:
            result = maintain_log_params.PackageLogExportTaskResponse()
            result.init_all_attr()
            result.user_session = ''
            result.return_code = err_code_mgr.ER_MAINTAINLOG_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_MAINTAINLOG_INVALID_DESERIALIZE_ERROR
                                                            , cmd='PackageLogExportTaskQueryHandler')
            result.tasks = []            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return
        
        result = self.get_worker().get_maintain_log_manager().query_export_task(req)
        
        self.get_worker().get_app().send_ack(frame, (result.serialize(), ))
        
class ZipLogFileTimeoutHandler(bf.TimeOutHandler):
    """
    Class: ZipLogFileTimeoutHandler
    Description: ���ڽ���ת����־ѹ������
    Base: TimeOutHandler
    Others: ��
    """

    def time_out(self):
        """
        Method: time_out
        Description: ���ڽ���ת����־ѹ������
        Parameter: ��
        Return: ��
        Others: ��
        """

        self.get_worker().get_maintain_log_manager().zip_file()
     