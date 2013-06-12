#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-07
Description: Linux系统加固，加固报告用户，用户口令策略，用户口令有效周期，系统服务，ssh加固。
Others: 无
Key Class&Method List: 
             1. check_user：检查是否存在不必要的用户
             2. delete_user:删除系统中不必存在的用户
             3. check_user_cycle:检查用户口令的有效周期
             4. reinforce_user_cycle：加固用户口令的有效周期
             5. check_user_strategy: 检查用户口令的策略是否存在风险
             6. reinforce_user_strategy: 加固用户口令的策略
             7. check_ssh_root：检查ssh是否存在可以用root用户登入的隐患
             8. check_ssh_port： 检查ssh端口是否为默认的22
             9. reinforc_ssh：加固ssh
             10. check_telnet：检查系统是否存在telnet服务，如果存在telnet是否被打开
             11. reinforce_telnet： 关闭telnet服务
             12. check_service：检查系统服务是否存在风险
             13. reinforce_service：加固系统服务
History: 
1. Date: 2013-03-07
   Author: ACP2013
   Modification: 新建文件
"""


import os
import subprocess
import re
import time

import tracelog

import reinforce_params

#检查当前用户
def check_user():
    """
    Function: check_user
    Description: 检查是否存在不必要的用户
    Parameter: 无
    Return: delusers,是一个列表，列表如果有数据，代表该用户为不必要的用户
    Others: 无
    """

    delusers = []
    execute_cmd = subprocess.Popen('cat /etc/passwd', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    execute_cmd.wait()
    if execute_cmd.returncode==0:
        user_details = execute_cmd.stdout.read()
        for user_need_del in ['news','uucp','games','gopher','mail','ftp']:
            if user_need_del in user_details:
                delusers.append(user_need_del)
    else:
        tracelog.error('Can not check user list')
        
    return delusers
            

#删除不必要的用户
def delete_user(delusers):
    """
    Function: delete_user
    Description: 删除不必要的用户
    Parameter: 
        delusers: 是一个列表，列表中的数据为需要删除的用户
    Return: return_code，0代表成功，非0代表失败
    Others: 无
    """

    return_code = 0
    for deluser in delusers:
        if os.system('userdel %s' %deluser)!=0:
            tracelog.error('Delete USER %s Failed' % deluser)
            return_code = 1
        else:
            tracelog.info('Delete USER %s Successful' % deluser)
    
    return return_code
            
#检查用户口令有效周期
def check_user_cycle():
    """
    Function: check_user_cycle
    Description: 检查用户口令的有效周期
    Parameter: 无
    Return: 1.user_cycle_line,修改后的配置文件语句，是一个列表
            2.user_set_problem,用户口令有效周期存在的问题,是一个列表
    Others: 无
    """

    user_cycle_line = []
    user_set_problem = []
    
    return_code,user_cycle_line = read_file(os.path.join('/etc/','login.defs'))
    if return_code!=0:
        user_set_problem.append('Can not Open File login.defs')
        return user_cycle_line,user_set_problem
    
    for line_index,line in enumerate(user_cycle_line):
        max_day = re.match(r'\s*PASS_MAX_DAYS\s+(\d+)', line)
        if max_day is None:
            continue
        max_day_re = max_day.group(1)
        if int(max_day_re)>reinforce_params.password_max_days:
            user_cycle_line[line_index] = 'PASS_MAX_DAYS   %s\n' % reinforce_params.password_max_days
            user_set_problem.append('Waring:The User validity we suggested is %s '
                                    'days and now it is %s days' %(
                                    reinforce_params.password_max_days,max_day_re))
        break
    else:
        user_set_problem.append('Waring:Do not find The User validity')
        user_cycle_line.append('PASS_MAX_DAYS   %s\n' % reinforce_params.password_max_days)
            
    return user_cycle_line,user_set_problem

#加固帐号口令有效周期
def reinforce_user_cycle(user_cycle_line):
    """
    Function: reinforce_user_cycle
    Description: 加固用户口令的有效周期
    Parameter: 
        user_cycle_line: 修改后的配置文件语句
    Return: return_code，0代表成功，非0代表失败
    Others: 无
    """

    
    return_code = write_file(os.path.join('/etc/','login.defs'),user_cycle_line)
    if return_code!=0:
        tracelog.exception('Reinforce User Cycle Failed')
        return 1

    return 0

#检查用户口令策略
def check_user_strategy():
    """
    Function: check_user_strategy
    Description: 检查用户口令的策略是否存在风险
    Parameter: 无
    Return: 1.user_strategy_line:修改后的配置文件语句
            2.strategy_problem:用户口令策略存在的问题
    Others: 无
    """

    user_strategy_line = []
    strategy_problem = []
    cracklib_search = True
    pam_unix_re_search = True
    
    file_patch = os.path.realpath(os.path.join('/etc/','pam.d','system-auth'))
    return_code,user_strategy_line = read_file(file_patch)
    if return_code!=0:
        strategy_problem.append('Can not Open File system-auth')
        return user_strategy_line,strategy_problem
    
    for line_index, line in enumerate(user_strategy_line):
        if cracklib_search is True:
            cracklib_re = re.match(r'\s*password\s+requisite\s+pam_cracklib.so', line)
            if cracklib_re is not None:
                minlen_re = re.search(r'minlen=(\d+)',line)
                minclass_re = re.search(r'minclass=(\d+)',line)
                if minlen_re is None:
                    strategy_problem.append('Waring: minline Risk exists in the User Strategy')
                    pwd_minline = reinforce_params.password_min_line
                else:
                    password_minlen = minlen_re.group(1)
                    if int(password_minlen) < reinforce_params.password_min_line:
                        strategy_problem.append('Waring: minline Risk exists in the User Strategy')
                        pwd_minline = reinforce_params.password_min_line
                    else:
                        pwd_minline = password_minlen
                    
                if minclass_re is None:
                    strategy_problem.append('Waring: minclass Risk exists in the User Strategy')
                    pwd_minclass = reinforce_params.password_minclass
                else:    
                    password_minclass = minclass_re.group(1)
                    if int(password_minclass) < reinforce_params.password_minclass:
                        strategy_problem.append('Waring: minclass Risk exists in the User Strategy')
                        pwd_minclass = reinforce_params.password_minclass
                    else:
                        pwd_minclass = password_minclass

                user_strategy_line[line_index] =('password    requisite     pam_cracklib.so '
                                                   'try_first_pass retry=5 minlen=%s minclass=%s\n' %(
                                                    pwd_minline,pwd_minclass))
                cracklib_search = False
                    
        if pam_unix_re_search is True:
            pam_unix_re = re.match(r'\s*password\s+sufficient\s+pam_unix.so', line)
            if pam_unix_re is not None:
                remember_re = re.search(r'remember=(\d+)', line)
                if remember_re is None:
                    strategy_problem.append('Waring:password remember Risk exists in the User Strategy')
                    user_strategy_line[line_index] = ('password    sufficient    pam_unix.so '
                                                        'sha512 shadow nullok try_first_pass '
                                                        'use_authtok remember=%s\n' %(
                                                        reinforce_params.password_remember))
                else:
                    password_remember = remember_re.group(1)
                    if int(password_remember) < reinforce_params.password_remember:
                        strategy_problem.append('Waring:password remember Risk exists in the User Strategy')
                        user_strategy_line[line_index] = ('password    sufficient    pam_unix.so '
                                                            'sha512 shadow nullok try_first_pass '
                                                            'use_authtok remember=%s\n' %(
                                                            reinforce_params.password_remember))
                pam_unix_re_search = False
                
        if pam_unix_re_search is False and cracklib_search is False:
            break
            
    return user_strategy_line,strategy_problem

#加固用户口令策略
def reinforce_user_strategy(user_strategy_line):
    """
    Function: reinforce_user_strategy
    Description: 加固用户口令的策略
    Parameter: 
        user_strategy_line: 修改后的配置文件语句
    Return: return_code，0代表成功，非0代表失败
    Others: 无
    """

    file_patch = os.path.realpath(os.path.join('/etc/','pam.d','system-auth'))
    return_code = write_file(file_patch,user_strategy_line)
    if return_code!=0:
        tracelog.exception('Reinforce User Strategy Failed')
        return 1

    return 0

#检查root用户ssh登入
def check_ssh_root():
    """
    Function: check_ssh_root
    Description: 检查ssh是否存在可以用root用户登入的隐患
    Parameter: 无
    Return: 1.ssh_line：修改后的配置文件语句
            2.ssh_problem:ssh存在的问题
    Others: 无
    """

    ssh_line = []
    ssh_problem = []
    
    return_code,ssh_line = read_file(os.path.join('/etc/','ssh','sshd_config'))
    if return_code!=0:
        ssh_problem.append('Can not Open File sshd_config')
        return ssh_line,ssh_problem
        
    for line_index, line in enumerate(ssh_line):
        root_re = re.match(r'\s*PermitRootLogin\s+(\w+)', line)
        if root_re is None:
            continue
        ssh_root = root_re.group(1)
        if ssh_root.lower()=='yes':
            ssh_problem.append('Waring:The root can through SSH login system')
            ssh_line[line_index] = 'PermitRootLogin no\n'
        break
    else:
        ssh_problem.append('Waring:The root can through SSH login system')
        ssh_line.append('PermitRootLogin no\n')
        
    return ssh_line,ssh_problem

#检查ssh的端口号
def check_ssh_port():
    """
    Function: check_ssh_port
    Description: 检查ssh端口是否为默认的22
    Parameter: 无
    Return: 1.ssh_line:修改后的配置文件语句
            2.ssh_problem:ssh存在的问题
    Others: 无
    """

    ssh_line = []
    ssh_problem = []
    line_index = 0
    
    return_code,ssh_line = read_file(os.path.join('/etc/','ssh','sshd_config'))
    if return_code!=0:
        ssh_problem.append('Can not Open File sshd_config')
        return ssh_line,ssh_problem
    
    for line_index, line in enumerate(ssh_line):
        root_re = re.match(r'\s*Port\s+(\d+)', line)
        if root_re is None:
            continue
        ssh_port = root_re.group(1)
        if int(ssh_port)!=reinforce_params.ssh_port:
            ssh_problem.append('Waring:SSH Port is not we suggested '
                               'and now the port is %s'% ssh_port)
            ssh_line[line_index] = 'Port %s\n' % reinforce_params.ssh_port
        break
    else:
        ssh_problem.append('Waring:SSH Port is not we suggested and now the port is 22')
        ssh_line.append('Port %s\n' % reinforce_params.ssh_port)
        
    return ssh_line,ssh_problem

#加固ssh，包括禁止root用户登入，更改端口
def reinforc_ssh(ssh_line):
    """
    Function: reinforc_ssh
    Description: 加固ssh
    Parameter: 
        ssh_line: 修改后的ssh配置文件语句
    Return: return_code，0代表成功，非0代表失败
    Others: 无
    """

    return_code = write_file(os.path.join('/etc/','ssh','sshd_config'),ssh_line)
    if return_code!=0:
        tracelog.exception('Reinforce SSH Strategy Failed')
        return 1

    return restart_service('sshd')

#检查系统服务                
def check_service():
    """
    Function: check_service
    Description: 检查系统服务是否存在风险
    Parameter: 无
    Return: 1.service_should_on:检查后，认为需要打开的系统服务
            2.service_should_off:检查后，任务需要关闭的系统服务
    Others: 无
    """

    service_should_off = []
    service_should_on = []
    
    check_service_on_list = ['NetworkManager','auditd','autofs','cpuspeed','crond','haldaemon','firstboot','iptables',
                           'mcstrans','mdmonitor','messagebus','microcode_ctl','netfs','network','nfs','nfslock',
                           'psacct','restorecond','rpcgssd','rpcidmapd','saslauthd','rsyslog','smartd','xfs']
    check_service_off_list = ['acpid','atd','avahi-daemon','cups','dnsmasq','ip6tables','rpcsvcgssd','vncserver','vsftpd']
    
    #为了能够检查，把语言更改为英语
    os.environ['LANG']='uc_EN'
    
    for service in check_service_on_list:
        if check_service_on(service) is True:
            service_should_on.append(service)
    
    for service in check_service_off_list:
        if check_service_off(service) is True:        
            service_should_off.append(service)
    
    return service_should_on,service_should_off

#加固系统服务
def reinforce_service(service_on,service_off):
    """
    Function: reinforce_service
    Description: 加固系统服务
    Parameter: 
        service_on: 需要打开的系统服务列表
        service_off: 需要关闭的系统服务列表
    Return: return_code，0代表成功，非0代表失败
    Others: 无
    """

    return_code = 0
    for service in service_on:
        for u in xrange(3):
            if os.system("service %s start" % service) != 0:
                tracelog.error('Fail to start service %s and have tried %u' %(service,u))
                time.sleep(1)
            else:
                tracelog.info('%s service start' % service)
                break
        else:
            return_code = 1
        for u in xrange(3):
            if os.system("chkconfig %s on" % service) != 0:
                tracelog.error('Fail to set service %s on and have tried %u' %(service,u))
                time.sleep(1)
            else:
                tracelog.info('%s service set on' % service)
                break  
        else:
            return_code = 1
            
    for service in service_off:
        for u in xrange(3):
            if os.system("service %s stop" % service) != 0:
                tracelog.error('Fail to stop service %s and have tried %u' %(service,u))
                time.sleep(1)
            else:
                tracelog.info('%s service stop' % service)
                break
        else:
            return_code = 1
        for u in xrange(3):
            if os.system("chkconfig %s off" % service) != 0:
                tracelog.error('Fail to set service %s off and have tried %u' %(service,u))
                time.sleep(1)
            else:
                tracelog.info('%s service set off' % service)
                break  
        else:
            return_code = 1 
                
    return return_code

#查看是否有telnet服务 ?返回值处理？
def check_telnet():
    """
    Function: check_telnet
    Description: 检查系统是否存在telnet服务，如果存在telnet是否被打开 
    Parameter: 无
    Return:True代表存在telnet风险
    Others: 无
    """

    check_cmd = subprocess.Popen('rpm -qa|grep telnet-server', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    check_cmd.wait()
    if check_cmd.returncode!=0:
        return False
    os.environ['LANG']='uc_EN'
    check_cmd = subprocess.Popen('chkconfig --list telnet', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    check_cmd.wait()
    if check_cmd.returncode==0:
        if 'on' in check_cmd.stdout.read():
            return True
        else:
            return False
    else:
        tracelog.error('Can not check telnet')
        return False

#如果telnet服务开启那么对其关闭    
def reinforce_telnet():
    """
    Function: reinforce_telnet
    Description: 关闭telnet服务
    Parameter: 无
    Return: return_code，0代表成功，非0代表失败
    Others: 无
    """
    
    return_code = 0
    for u in xrange(3):
        if os.system("service telnet stop") != 0:
            tracelog.error('Fail to stop service telnet and have tried %u' %(u))
            time.sleep(1)
        else:
            tracelog.info('telnet service stop')
            break
    else:
        return_code = 1
    for u in xrange(3):
        if os.system("chkconfig telnet off") != 0:
            tracelog.error('Fail to set service telnet off and have tried %u' %(u))
            time.sleep(1)
        else:
            tracelog.info('telnet service set off')
            break  
    else:
        return_code = 1 
            
    return return_code
    

#检查应该开启的服务是否开启    
def check_service_off(service_name):
    """
    Function: check_service_off
    Description: 检查应该关闭的服务是否关闭
    Parameter: 
        service_name: 服务名称
    Return: service_should_off,true代表该服务没有关闭，需要关闭
    Others: 无
    """

    service_should_off = True
    check_cmd = subprocess.Popen('chkconfig --list %s' %service_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    check_cmd.wait()
    if check_cmd.returncode==0:
        if '3:off\t4:off\t5:off' in check_cmd.stdout.read():
            service_should_off = False
    else:
        tracelog.error('Execute chkconfig %s Failed' %service_name )
    return service_should_off

#检查应该关闭的服务是否关闭
def check_service_on(service_name):
    """
    Function: check_service_on
    Description: 检查应该打开的服务是否打开
    Parameter: 
        service_name: 服务名称
    Return: service_should_on,true代表该服务关闭了，需要打开
    Others: 无
    """

    service_should_on = True
    check_cmd = subprocess.Popen('chkconfig --list %s' %service_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    check_cmd.wait()
    if check_cmd.returncode==0:
        if '3:on\t4:on\t5:on' in check_cmd.stdout.read():
            service_should_on = False
    else:
        tracelog.error('Execute chkconfig %s Failed' %service_name )
    return service_should_on

#读取配置文件         
def read_file(file_patch):
    """
    Function: read_file
    Description: 读取配置文件
    Parameter: 
        file_patch: 文件路径
    Return: 元组，第一个元素代表是否成功,user_set是配置文件的语句
    Others: 无
    """

    openfile = None
    user_set = []
    try:
        openfile = open(file_patch,'r')
        user_set = openfile.readlines()
    except Exception, err:
        tracelog.exception('Can not Open %s and the err is %s'%(file_patch,err))
        return 1,user_set
    finally:
        if openfile is not None:
            openfile.close()
    return 0,user_set

#备份文件并且写入配置文件
def write_file(file_patch,user_set):
    """
    Function: write_file
    Description: 写入配置文件
    Parameter: 
        file_patch: 文件路径
        user_set: 配置文件语句
    Return: 0代表成功，1代表失败
    Others: 无
    """

    openfile = None
    try:
        if os.path.exists('%s.bak'%file_patch):
            os.remove('%s.bak'%file_patch)
        os.rename(file_patch, '%s.bak'%file_patch)
    except Exception, err:
        tracelog.exception('Can not backup file and err is %s' %err)
        return 1

    try:
        openfile = open(file_patch,'w+')
        for i in user_set:
            openfile.write(i)
    except Exception, err:
        tracelog.exception('Write file error %s and the err is %s'%(file_patch,err))
        if os.path.exists(file_patch):
            os.remove(file_patch)
        os.rename('%s.bak'%file_patch, file_patch)
        return 1
    finally:
        if openfile is not None:
            openfile.close()
    return 0

#重启系统服务
def restart_service(service_name):
    """
    Function: restart_service
    Description: 重启系统服务
    Parameter: 
        service_name: 系统服务名称
    Return: 0代表成功，1代表失败
    Others: 无
    """

    for i in xrange(3):
        if os.system('service %s restart'%service_name) != 0:
            tracelog.error('Fail to restart %s and have tried %d' %(service_name,i))
            time.sleep(1)
        else:
            tracelog.info('%s service restart'%service_name)
            break
    else:
        return 1
    
    return 0
    
#命令行
def os_execute(os_line):
    """
    Function: os_execute
    Description: 执行命令行
    Parameter: 
        os_line: 要执行的命令语句
    Return: 0代表成功，1代表失败
    Others: 无
    """

    for u in xrange(3):
        execute_cmd = subprocess.Popen(os_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        execute_cmd.wait()
        if execute_cmd.returncode != 0:
            tracelog.error('Fail to execute %s and have tried %d' %(os_line,u))
            tracelog.error(execute_cmd.stdout.readline())                
            time.sleep(1)
        else:
            return 0
    else:
        return 1