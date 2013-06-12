#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-22
Description: event manager�����붨���ļ�
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:2012-11-22
   Author:ACP2013
   Modification:�½��ļ�
"""


#OSS ������
OSS_BASE = 0x02000000

#һ��APP����0x1000��������
EVENT_REPORT_BASE = 0x0






########################################################################
#EVENT MANAGER COMMAND CODE
########################################################################
"""
EVENT_REPORT_COMMAND
data����1������
event_data:�ϱ�event����,pickle����
û�з�����Ϣ
"""
EVENT_REPORT_COMMAND = OSS_BASE + EVENT_REPORT_BASE + 0


"""
EVENT_QUERY_REQUEST
data����1������
query_req:EventQueryRequest ��JSON����
���� EventQueryResponse ��JSON����
"""
EVENT_QUERY_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 1

"""
EVENT_EXPORT_REQUEST
data����1������
query_req:EventQueryRequest ��JSON����
���� EventQueryResponse ��JSON����
"""
EVENT_EXPORT_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 2

"""
EVENT_EXPORT_TASK_QUERY_REQUEST
data����1������
query_req:EventQueryRequest ��JSON����
���� EventQueryResponse ��JSON����
"""
EVENT_EXPORT_TASK_QUERY_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 3

"""
EVENT_FILTER_LIST_REQUEST
data��û�в���
���� EventFilterListResponse ��JSON����
"""
EVENT_FILTER_LIST_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 4

"""
EVENT_IMC_QUERY_EAU_REQUEST
data����1������
query_req:EventImcQueryEauRequest ��JSON����
���� EventQueryResponse ��JSON����
"""
EVENT_IMC_QUERY_EAU_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 5

"""
EVENT_QUERY_TO_IMC_REQUEST,��Ϣ��ʽͬ EVENT_QUERY_REQUEST������IMC��EAU��ѯ
"""
EVENT_QUERY_TO_IMC_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 6

"""
WEB_EVENT_REPORT_COMMAND������WEB���ģ����event manager�����¼�

"""
WEB_EVENT_REPORT_COMMAND = OSS_BASE + EVENT_REPORT_BASE + 7

if __name__=='__main__':
    print EVENT_QUERY_REQUEST, EVENT_EXPORT_REQUEST, EVENT_EXPORT_TASK_QUERY_REQUEST, EVENT_IMC_QUERY_EAU_REQUEST, WEB_EVENT_REPORT_COMMAND

