#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��н�����ͬ�����ܴ���ʹ�õ�������ģ���·�����뵽sys.path��
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


paths=["../../../rfid_plt/base_platform"
    , "../../../rfid_plt/plt_common"
    , "../../../share_libs"
    , "../../../moc_def"
    , "../../../rfid_plt/base_platform/db_sync"
    , "../../../rfid_plt/db_sync"
    ]

import sys
import os.path

cur_dir = os.path.dirname(__file__)
for p in paths:        
    sys.path.append(os.path.join(cur_dir, p))
