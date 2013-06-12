#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-07
Description: 系统加固防火墙设置部分
Others: 无
Key Class&Method List: 
             1. IptablesReinforce，类，负责防火墙设置
History: 
1. Date:2013-03-07
   Author:ACP2013
   Modification:新建文件
"""


import os
import time
import subprocess

import tracelog

from reinforce_module import write_file
from reinforce_module import read_file
from reinforce_module import restart_service
from reinforce_module import os_execute

iptables_patch = os.path.join('/etc/','sysconfig','iptables')

class IptablesReinforce():
    """
    Class: IptablesReinforce
    Description: 负责防火墙设置
    Base: 无
    Others: 无
    """

    def __init__(self):
        """
        Method: __init__
        Description: 初始化，包括默认端口设置
        Parameter: 无
        Return: 无
        Others: 无
        """

        self.__inner = []
        self.__external = []
        self.__all = []
        self.__inner_network_card = []
        self.__external_network_card = []
        self.__all_network_card = []
        self.reinforce_iptables()
        
    #设置网卡
    def set_network_card(self,cards):
        """
        Method: set_network_card
        Description: 设置网卡
        Parameter: 
            cards: 网卡名称
        Return: 无
        Others: inner代表内部网卡,external代表外部网卡,all代表内部外部都能访问的网卡
        """

        for card in cards:
            if card[1]=='inner':
                self.__inner_network_card.append(card[0])
            elif card[1]=='external':
                self.__external_network_card.append(card[0])
            else:
                self.__all_network_card.append(card[0])
        
    def reinforce_iptables(self):
        """
        Method: reinforce_iptables
        Description: 默认端口设置
        Parameter: 无
        Return: 无
        Others: 无
        """

        #默认对内端口
        self.__inner.append(['6000','udp'])
        self.__inner.append(['6001','tcp'])
        self.__inner.append(['6100:6999','tcp'])
        
        #默认对外端口
        self.__external.append(['80','tcp'])
        self.__external.append(['7000:7003','tcp'])
        self.__external.append(['7100:7900','tcp'])
        self.__external.append(['8000:8999','tcp'])
    
    #提供用户自定义接口
    def set_custom_iptables(self,custom_rules):
        """
        Method: set_custom_iptables
        Description: 用户自定义端口设置
        Parameter: 
            custom_rules: 用户规则，是一个列表，列表中的元素是元组，元组的格式如下:("端口号","tcp或者udp","网卡是内部还是外部")
        Return: 无
        Others: 无
        """

        for custom_rule in custom_rules:
            if custom_rule[2]=='inner':
                self.__inner.append([custom_rule[0],custom_rule[1]])
            elif custom_rule[2]=='external':
                self.__external.append([custom_rule[0],custom_rule[1]])
            else:
                self.__all.append([custom_rule[0],custom_rule[1]])
                
    def iptables_take_effect(self):
        """
        Method: iptables_take_effect
        Description: 防火墙生效
        Parameter: 无
        Return: 0代表成功，非0代表失败
        Others: 无
        """

        iptables_setline =['*filter\n']
        iptables_setline.append(':INPUT DROP [0:0]\n')
        iptables_setline.append(':FORWARD DROP [0:0]\n')
        iptables_setline.append(':OUTPUT ACCEPT [0:0]\n')
           
        for inner in self.__inner:
            for card in self.__inner_network_card:
                iptables_setline.append('-A INPUT -i %s -p %s -m %s --dport %s -j ACCEPT\n'%(
                                        card,inner[1],inner[1],inner[0]))
        for external in self.__external:
            for card in self.__external_network_card:
                iptables_setline.append('-A INPUT -i %s -p %s -m %s --dport %s -j ACCEPT\n'%(
                                        card,external[1],external[1],external[0]))
        for all_line in self.__all:
            for card in self.__all_network_card:
                iptables_setline.append('-A INPUT -i %s -p %s -m %s --dport %s -j ACCEPT\n'%(
                                        card,all_line[1],all_line[1],all_line[0]))
        
        iptables_setline.append('-A INPUT -p icmp -j ACCEPT\n')
        iptables_setline.append('-A INPUT -i lo -p all -j ACCEPT\n')       
        iptables_setline.append('COMMIT\n')
        
        return_code = write_file(iptables_patch,iptables_setline)
        if return_code!=0:
            tracelog.exception('reinforce_iptables Failed')
            return 1
        
        return restart_service('iptables')
    
    #添加防火墙记录
    def add_iptables_rule(self,rule):
        """
        Method: add_iptables_rule
        Description: 添加防火墙规则的原子操作
        Parameter: 
            rule: 规则，是个三元组，格式如下("网卡名称","tcp或udp","端口号")
        Return: 0代表成功，1代表失败
        Others: 无
        """

        return_code = os_execute("iptables -A INPUT -i %s -p %s --dport %s -j ACCEPT" %(
                                rule[0],rule[2],rule[1]))
        if return_code !=0:
            tracelog.error('Fail to add iptables rule')
            return 1
        else:
            tracelog.info('iptables add and info is %s card %s port %s treaty'%(
                            rule[0],rule[2],rule[1]))
        
        return_code = os_execute("service iptables save")
        if return_code !=0:
            tracelog.error('Fail to save iptables rule')
            return 1
        else:
            tracelog.info('Success to save iptables')
            
        return 0
    
    #删除防火墙规则
    def del_iptables_rule(self,rule):       
        """
        Method: del_iptables_rule
        Description: 删除防火墙设置的原子操作
        Parameter: 
            rule: 防火墙规则，是个三元组，格式如下("网卡名称","tcp或udp","端口号")
        Return: 0代表成功，1代表失败
        Others: 无
        """

        #删除
        return_code = os_execute("iptables -D INPUT -i %s -p %s --dport %s -j ACCEPT" %(
                                rule[0],rule[2],rule[1]))
        
        if return_code !=0:
            tracelog.error('Fail to del iptables rule')
            return 1
        else:
            tracelog.info('iptables rule deleted and info is %s card %s port %s treaty'%(
                            rule[0],rule[2],rule[1]))
        
        
        return_code = os_execute("service iptables save")
        if return_code !=0:
            tracelog.error('Fail to save iptables rule')
            return 1
        else:
            tracelog.info('Success to save iptables')
            
        return 0
    
    #修改防火墙规则
    def mod_iptables_rule(self,oldrule,new_state):
        """
        Method: mod_iptables_rule
        Description: 修改防火墙设置的原子操作
        Parameter: 
            oldrule: 旧规则，是个三元组，格式如下("网卡名称","tcp或udp","端口号")
            new_state: 新规则的状态，状态可以是 DROP,ACCEPT
        Return: 0代表成功，1代表失败
        Others: 无
        """

        #删除
        return_code = os_execute("iptables -D INPUT -i %s -p %s --dport %s -j ACCEPT" %(
                                oldrule[0],oldrule[2],oldrule[1]))
        
        if return_code !=0:
            tracelog.error('Fail to del iptables rule')
            return 1
        else:
            tracelog.info('iptables rule deleted and info is %s card %s port %s treaty'%(
                            oldrule[0],oldrule[2],oldrule[1]))
            
        return_code = os_execute("iptables -A INPUT -i %s -p %s --dport %s -j %s" %(
                                oldrule[0],oldrule[2],oldrule[1],new_state))
        if return_code !=0:
            tracelog.error('Fail to add iptables rule')
            return 1
        else:
            tracelog.info('iptables add and info is card:%s port:%s treaty:%s state:%s '%(
                            oldrule[0],oldrule[2],oldrule[1],new_state))
        
        
        return_code = os_execute("service iptables save")
        if return_code !=0:
            tracelog.error('Fail to save iptables rule')
            return 1
        else:
            tracelog.info('Success to save iptables')
        
        return 0