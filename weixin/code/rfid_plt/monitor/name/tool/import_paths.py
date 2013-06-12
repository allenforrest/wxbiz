#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-03
Description: 运行环境所需的路径设置
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:2012-12-03
   Author:ACP2013
   Modification:新建文件
"""

paths=["../../../base_platform"
    , "../../../plt_common"
    , "../../../../share_libs"
    , "../../../../moc_def"]

import sys
import os.path

cur_dir = os.path.dirname(__file__)
for p in paths:        
    sys.path.append(os.path.join(cur_dir, p))
