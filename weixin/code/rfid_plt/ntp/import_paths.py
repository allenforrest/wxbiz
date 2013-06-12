#coding=gbk

paths=["../../rfid_plt/base_platform"
    , "../../rfid_plt/plt_common"
    , "../../share_libs"
    , "../../moc_def/moc_ntpd"
    , "../../moc_def"
    ]

import sys
import os.path

cur_dir = os.path.dirname(__file__)
for p in paths:        
    sys.path.append(os.path.join(cur_dir, p))
