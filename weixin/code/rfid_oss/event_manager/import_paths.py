#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: 用于加载运行时的路径
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:新建文件
"""

paths=["../../rfid_plt/base_platform"
    , "../../rfid_plt/plt_common"
    , "../../share_libs"
    , "../../rfid_common"
    , "../../moc_def"
    ]

import sys
import os.path

cur_dir = os.path.dirname(__file__)
for p in paths:        
    sys.path.append(os.path.join(cur_dir, p))
