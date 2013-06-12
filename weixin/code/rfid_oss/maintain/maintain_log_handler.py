#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: maintain log的定时维护，log按日期打包，log打包任务情况查询
Others:无
Key Class&Method List: 
             1. PackageLogHandler：负责日志打包
             2. PackageLogExportTaskQueryHandler： 负责打包任务情况查询
             3. ZipLogFileTimeoutHandler： 定期进行转储日志压缩工作
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:新建文件
"""



import bundleframework as bf
import tracelog
import err_code_mgr

import maintain_log_params


class PackageLogHandler(bf.CmdHandler):    
    """
    Class: PackageLogHandler
    Description: 日志打包
    Base: CmdHandler
    Others: 无
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 日志打包
        Parameter: 
            frame: 收到的处理消息
            data区1个参数：
            msg：PackageLog对象
        Return: 无
        Others: 无
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
    Description: 打包任务情况查询
    Base: CmdHandler
    Others: 无
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 打包任务情况查询
        Parameter: 
            frame: 收到的处理消息
            data区1个参数：
            msg：PackageLogExportTaskRequest对象 
        Return: 无
        Others: 无
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
    Description: 定期进行转储日志压缩工作
    Base: TimeOutHandler
    Others: 无
    """

    def time_out(self):
        """
        Method: time_out
        Description: 定期进行转储日志压缩工作
        Parameter: 无
        Return: 无
        Others: 无
        """

        self.get_worker().get_maintain_log_manager().zip_file()
     