#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-21
Description: 
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:2012-11-21
   Author:ACP2013
   Modification:新建文件
"""

import os
import os.path
import sys
import time

if __name__ == "__main__":
    import import_paths
    
import mit

from moc_name_service import AppType
from moc_name_service import AppInstance


if __name__=='__main__':
    mit_manager = mit.Mit()
    
    mit_manager.regist_moc(AppType.AppType, AppType.AppTypeRule)
    mit_manager.regist_moc(AppInstance.AppInstance, AppInstance.AppInstanceRule)    
    
    db_file_path = "../../nameservice.db"
    #清空所有
    try:
        os.remove(db_file_path)
    except:
        pass
    
    mit_manager.open_sqlite(db_file_path)
    
    param_rdm = mit_manager.gen_rdm('AppType')
    param_rdm.service_name = 'Monitor'
    param_rdm.instance_num = 1    
    mit_manager.rdm_add(param_rdm)
    
    param_rdm.service_name = 'AleReportApp'
    param_rdm.instance_num = 4    
    mit_manager.rdm_add(param_rdm)
    
    param_rdm.service_name = 'EventManagerApp'
    param_rdm.instance_num = 1    
    mit_manager.rdm_add(param_rdm)
    
    
    
    
    