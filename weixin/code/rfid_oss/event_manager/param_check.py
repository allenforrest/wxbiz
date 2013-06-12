#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-1-22
Description: event manager 参数检查文件
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:2013-1-22
   Author:ACP2013
   Modification:新建文件
"""

import err_code_mgr

def check_page(current_page, num_per_page, max_query_records_per_page):
    return_code = err_code_mgr.ER_SUCCESS
    description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
    
    #current_page 参数检查
    if current_page is None:
        return_code = err_code_mgr.ER_NO_CURRENT_PAGE_PARAMETER
        description = err_code_mgr.get_error_msg(err_code_mgr.ER_NO_CURRENT_PAGE_PARAMETER)
    
    #num_per_page 参数检查
    elif num_per_page is None:
        return_code = err_code_mgr.ER_NO_NUM_PER_PAGE_PARAMETER
        description = err_code_mgr.get_error_msg(err_code_mgr.ER_NO_NUM_PER_PAGE_PARAMETER)
    
    elif num_per_page<=0 or num_per_page>max_query_records_per_page:
            return_code = err_code_mgr.ER_NUM_PER_PAGE_OUT_OF_SCOPE
            description = err_code_mgr.get_error_msg(err_code_mgr.ER_NUM_PER_PAGE_OUT_OF_SCOPE, value=num_per_page)
                        
    return return_code, description
    
    
def check_filter(event_filter):
    return_code = err_code_mgr.ER_SUCCESS
    description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
    
    #event_filter 参数检查
    if event_filter is None:
        return_code = err_code_mgr.ER_NO_EVENT_FILTER_PARAMETER
        description = err_code_mgr.get_error_msg(err_code_mgr.ER_NO_EVENT_FILTER_PARAMETER)
    
    #start_time 和 end_time 参数检查
    elif event_filter.start_time is not None and event_filter.start_time<0:
        return_code = err_code_mgr.ER_NEGATIVE_START_TIME
        description = err_code_mgr.get_error_msg(err_code_mgr.ER_NEGATIVE_START_TIME                                                                
                                                        , start_time=event_filter.start_time)
    elif event_filter.end_time is not None and event_filter.end_time<0:
        return_code = err_code_mgr.ER_NEGATIVE_END_TIME
        description = err_code_mgr.get_error_msg(err_code_mgr.ER_NEGATIVE_END_TIME                                                                
                                                        , end_time=event_filter.end_time)
        
    elif (event_filter.start_time is not None 
        and event_filter.end_time is not None 
        and event_filter.start_time> event_filter.end_time):
        return_code = err_code_mgr.ER_END_LESS_START
        description = err_code_mgr.get_error_msg(err_code_mgr.ER_END_LESS_START
                                                        , end_time=event_filter.end_time
                                                        , start_time=event_filter.start_time)
    return return_code, description