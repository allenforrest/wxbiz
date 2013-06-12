#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-12
Description: 
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""

import sys
sys.path.append(__path__[0] + '/transport')

import err_code_mgr
from _bundleframework import local_error_code
err_code_mgr.regist_errors(local_error_code.error_defs)

