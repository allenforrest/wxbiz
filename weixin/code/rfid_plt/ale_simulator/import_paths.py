#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-16
Description: 
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""

paths=["../../rfid_plt/base_platform"
    , "../../rfid_plt/plt_common"
    , "../../share_libs"
    , "../../rfid_app/reader_gateway/common"
    , "../../rfid_app/reader_gateway/llrp_reader_gateway"
    , "../../rfid_app/reader_message"
    , "../../rfid_app/control_manager/ale"
    , "../../rfid_app/control_manager/mit"
    , "../../rfid_app/control_manager/llrp"
    , "../../rfid_app/control_manager/common_reader"
    , "../../rfid_app/common_define"    
    ]

import sys
import os.path

cur_dir = os.path.dirname(__file__)
for p in paths:        
    sys.path.append(os.path.join(cur_dir, p))
