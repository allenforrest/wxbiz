#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-19
Description: 本文中实现了进程状态管理类
Others:      
Key Class&Method List: 
             1. ProcessStat: 单个进程的状态
             2. ProcessStatMgr: 进程状态管理类
History: 
1. Date:
   Author:
   Modification:
"""

import collections
import subprocess 
import time
from threading import RLock
import os.path

import bundleframework as bf
import tracelog


PROCESS_STARTING_TIMEOUT = 20
PROCESS_INITIALIZING_TIMEOUT = 600
PROCESS_RUNNING_TIMEOUT = 5
PROCESS_STOPPING_TIMEOUT = 2

import bundleframework as bf


class ProcessStat:
    """
    Class: ProcessStat
    Description: 单个进程的状态
    Base: 
    Others: 
    """

    STAT_PROCESS_STARTING       = 0  # 正在启动(monitor开始启动某个进程)
    STAT_PROCESS_INITIALIZING   = 1  # 正在初始化
    STAT_PROCESS_RUNNING        = 2  # 正常运行中
    STAT_PROCESS_STOPPING       = 3  # 正在停止
    STAT_PROCESS_STOPPED        = 4  # 已经停止
    
    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
        """

        # 进程的pid，在进程启动后，通过握手消息得到进程的pid
        self.__pid = bf.INVALID_PID

        # 进程的名字
        self.__process_name = ""
        
        # 进程的实例号，是系统内多实例的编号
        self.__instance_id = 0

        # 当前的运行状态
        self.__cur_stat = ProcessStat.STAT_PROCESS_STOPPED

        # 启动时，是否需要独占的一段时间
        # 以便可以先启动本进程，再启动其他进程
        self.__start_excluded = False  

        # 是否自动启动
        self.__auto_run_on_master = True
        self.__auto_run_on_slave = True

        # 程序在磁盘上的位置
        self.__program_path = ""

        # 握手计数器
        self.__shake_hand = 0

        # subprocess.Popen的实例
        self.__popen_inst = None

    def get_pid(self):
        return self.__pid
        
    def set_name(self, name):
        """
        Method:    set_name
        Description: 设置进程的名称
        Parameter: 
            name: 进程的名称
        Return: 
        Others: 
        """

        self.__process_name = name

    def get_name(self):
        """
        Method:    get_name
        Description: 获取进程的名称
        Parameter: 无
        Return: 进程的名称
        Others: 
        """

        return self.__process_name
    
    def set_instance_id(self, instance_id):
        """
        Method:    set_instance_id
        Description: 设置进程的实例号
        Parameter: 
            name: 进程的实例号
        Return: 
        Others: 
        """

        self.__instance_id = instance_id

    def get_instance_id(self):
        """
        Method:    get_name
        Description: 获取进程的实例号
        Parameter: 无
        Return: 进程的实例号
        Others: 
        """

        return self.__instance_id

    def set_starting(self):
        """
        Method:    set_starting
        Description: 设置进程的状态为正在启动中
        Parameter: 无
        Return: 
        Others: 
        """

        self.__cur_stat = ProcessStat.STAT_PROCESS_STARTING
        
    def is_starting(self):
        """
        Method:    is_starting
        Description: 判断进程是否正在启动中
        Parameter: 无
        Return: 进程是否正在启动中
        Others: 
        """

        return self.__cur_stat == ProcessStat.STAT_PROCESS_STARTING

    def set_initializing(self):
        """
        Method:    set_initializing
        Description: 设置进程的状态为正在初始化中
        Parameter: 无
        Return: 进程的状态为正在初始化中
        Others: 
        """

        self.__cur_stat = ProcessStat.STAT_PROCESS_INITIALIZING
    
    def is_initializing(self):
        """
        Method:    is_initializing
        Description: 判断进程是否正在初始化
        Parameter: 无
        Return: 进程是否正在初始化
        Others: 
        """

        return self.__cur_stat == ProcessStat.STAT_PROCESS_INITIALIZING

    def set_running(self):
        """
        Method:    set_running
        Description: 设置进程为正常运行中
        Parameter: 无
        Return: 
        Others: 
        """

        self.__cur_stat = ProcessStat.STAT_PROCESS_RUNNING
        
    def is_running(self):
        """
        Method:    is_running
        Description: 判断进程是否正常运行中
        Parameter: 无
        Return: 进程是否正常运行中
        Others: 
        """

        return self.__cur_stat == ProcessStat.STAT_PROCESS_RUNNING

    def set_stopping(self):
        """
        Method:    set_stopping
        Description: 设置进程的状态为正在停止
        Parameter: 无
        Return: 
        Others: 
        """

        self.__cur_stat = ProcessStat.STAT_PROCESS_STOPPING
        
    def is_stopping(self):
        """
        Method:    is_stopping
        Description: 判断进程的状态是否为正在停止
        Parameter: 无
        Return: 
        Others: 
        """

        return self.__cur_stat == ProcessStat.STAT_PROCESS_STOPPING

    def __set_stoped(self):
        """
        Method:    __set_stoped
        Description: 设置进程的状态为已经停止
        Parameter: 无
        Return: 
        Others: 
        """

        self.__cur_stat = ProcessStat.STAT_PROCESS_STOPPED

    def is_stopped(self):
        """
        Method:    is_stopped
        Description: 判断进程的状态是否为已经停止
        Parameter: 无
        Return: 
        Others: 
        """

        return self.__cur_stat == ProcessStat.STAT_PROCESS_STOPPED

    
    def set_exculde(self, is_exclude):
        """
        Method:    set_exculde
        Description: 设置进程启动时是否是排他的
        Parameter: 
            is_exclude: 布尔值, 进程启动时是否是排他的
        Return: 
        Others: 
        """

        self.__start_excluded = is_exclude
        
    def is_exclude(self):
        """
        Method:    is_exclude
        Description: 判断进程启动时是否是排他的
        Parameter: 无
        Return: 
        Others: 
        """

        return self.__start_excluded

    def set_auto_run(self, is_auto_run_on_master, is_auto_run_on_slave):
        """
        Method:    set_auto_run
        Description: 设置进程是否是自动的运行的
        Parameter: 
            is_auto_run_on_master: 布尔值，进程在master上是否是自动的运行的
            is_auto_run_on_slave: 布尔值，进程在slave上是否是自动的运行的
        Return: 
        Others: 
        """

        self.__auto_run_on_master = is_auto_run_on_master
        self.__auto_run_on_slave = is_auto_run_on_slave
        
    def is_auto_run_on_master(self):
        """
        Method:    is_auto_run_on_master
        Description: 判断进程在master上是否是自动的运行的
        Parameter: 无
        Return: 进程是否是自动的运行的
        Others: 
        """

        return self.__auto_run_on_master

    def is_auto_run_on_slave(self):
        """
        Method:    is_auto_run_on_slave
        Description: 判断进程在slave上是否是自动的运行的
        Parameter: 无
        Return: 进程是否是自动的运行的
        Others: 
        """

        return self.__auto_run_on_slave


    def set_program_path(self, program_path):
        """
        Method:    set_program_path
        Description: 设置软件程序在磁盘上的路径
        Parameter: 
            program_path: 软件程序在磁盘上的路径
        Return: 
        Others: 
        """

        self.__program_path = program_path


    def get_program_path(self):
        """
        Method:    get_program_path
        Description: 获取软件程序在磁盘上的路径
        Parameter: 无
        Return: 软件程序在磁盘上的路径
        Others: 
        """

        return self.__program_path
        

    def on_shake_hand(self, pid, statflag):
        """
        Method:    on_shake_hand
        Description: 当monitor收到握手消息后的响应函数
        Parameter: 
            statflag: 握手消息中带的状态标记
        Return: 
        Others: 
        """

        self.__shake_hand = 0
        self.__pid = pid

        if (statflag == bf.BasicApp.SHAKEHAND_INITIALIZING 
            and not self.is_initializing()):
            self.set_initializing()
            tracelog.info("process(%s) is initializing." % self.__process_name)  
            return

        elif (statflag == bf.BasicApp.SHAKEHAND_RUNNING 
            and not self.is_running()):
            self.set_running()
            tracelog.info("process(%s) is running." % self.__process_name)  
            return
        
        elif (statflag == bf.BasicApp.SHAKEHAND_STOPPING 
            and not self.is_stopping()):
            self.set_stopping()
            tracelog.info("process(%s) is stopping." % self.__process_name)  
            return

    def on_check_running(self):
        """
        Method:    on_check_running
        Description: 响应定时核查进程状态的函数
        Parameter: 无
        Return: 
        Others: 
        """

        if self.is_stopped():
            return
        
        # 如果程序是自动启动的，那么self.__popen_inst不为None，
        # 可以通过self.__popen_inst准确判断进程是否退出了
        if (self.__popen_inst is not None 
            and self.__popen_inst.poll() is not None):
            
            self.stop_process()
            return
            
        
        self.__shake_hand += 1

        # 如果是正在启动，那么如果超过一定时间未启动，则设置状态为停止
        if self.is_starting() and self.__shake_hand >= PROCESS_STARTING_TIMEOUT:
            tracelog.info("process(%s) start timeout." % self.__process_name)
            self.stop_process()
            return

        # 如果在初始化期间，超过一定的时间，则设置为停止
        if self.is_initializing() and self.__shake_hand >= PROCESS_INITIALIZING_TIMEOUT:
            tracelog.info("process(%s) initialize timeout." % self.__process_name)
            self.stop_process()
            return
                
        # 在运行期间，如果超过一定时间，则设置状态为停止
        if self.is_running() and self.__shake_hand >= PROCESS_RUNNING_TIMEOUT:
            tracelog.info("process(%s) is abnormal while running." % self.__process_name)
            self.stop_process()
            return

        if self.is_stopping() and self.__shake_hand >= PROCESS_STOPPING_TIMEOUT:
            #tracelog.error("process(%s) stopped." % self.__process_name)
            self.stop_process()
            return
       

    def start_process(self):
        """
        Method:    start_process
        Description: 启动进程
        Parameter: 无
        Return: 
        Others: 
        """
        program_path = self.__program_path
        if not os.path.exists(program_path):
            # py不存在，那么就使用pyc
            if program_path.endswith(".py") and os.path.exists(program_path + "c"):
                program_path +="c" 
            else:
                tracelog.error("program does not exist! program_path:%s"% self.__program_path)
                return 
                
        self.stop_process()       

        try:       
            # 注意: close_fds必须设置为True，否则子进程会继承父进程的文件句柄，导致父进程中文件无法正常重命名和删除
            # 例如log文件
            # 在windows中stdin、stdout、stderr必须不设置，否则close_fds无法设置为True
            self.__popen_inst = subprocess.Popen(["python", program_path, '--id=%s'%self.__instance_id]
                                , stdin=None #subprocess.PIPE
                                #, stdout=subprocess.PIPE
                                #, stderr=subprocess.PIPE
                                , close_fds = True
                                , cwd = os.path.dirname(program_path)
                                ) 
        except:
            tracelog.exception("start process failed. program path:%s"% program_path)
            return

        
        tracelog.info("starting process(%s, %d)  program path:%s"% (
                              self.__process_name
                            , self.__popen_inst.pid
                            , program_path))
                            
        self.set_starting() # 设置状态为 正在启动中
        

        
    def stop_process(self):
        """
        Method:    stop_process
        Description: 停止进程
        Parameter: 无
        Return: 
        Others: 
        """

        if self.__popen_inst is None:
            self.__set_stoped()            
            return

        try:   
            r = self.__popen_inst.poll()
            
            if r is None: # 仍在运行, 先尝试优雅关闭
                self.__popen_inst.terminate()

                # 等待10秒
                for i in xrange(20):
                    r = self.__popen_inst.poll()
                    if r is not None:
                        tracelog.info("process(%s, %d) is terminated." % (self.__process_name, self.__popen_inst.pid))
                        break

                    time.sleep(0.5)
                else:
                    self.__popen_inst.kill()  # kill进程
                    tracelog.info("process(%s, %d) is killed." % (self.__process_name, self.__popen_inst.pid))
            else:
                tracelog.info("process(%s, %d) stopped automatically." % (self.__process_name, self.__popen_inst.pid))
                
        except:
            tracelog.exception("exception happened while stop_process %s" % self.__process_name)

        self.__popen_inst = None
        self.__set_stoped()
        
        
class ProcessStatMgr:
    """
    Class: ProcessStatMgr
    Description: 进程状态管理类
    Base: 
    Others: 
    """

    STAT_HA_MASTER = 0      # 当前是master且有其他可用的slave
    STAT_HA_SLAVE = 1       # 当前是slave
    STAT_HA_ONLY_MASTER = 2 # 当前是master且没有其他可用的slave

    STAT_SYS_TO_START   = 0 # 等待启动
    STAT_SYS_RUNNING    = 1 # 正在运行
    STAT_SYS_TO_STOP    = 2 # 等待停止
    STAT_SYS_TO_RESTART = 3 # 等待重启
    STAT_SYS_STOPED     = 4 # 已经停止
    
    STAT_SYS_NONE       = 5 # 无状态
    
    __stat_ha = STAT_HA_ONLY_MASTER

    __process_stat_map = collections.OrderedDict() #process_name: ProcessStat

    __sys_cur_state  = STAT_SYS_TO_START
    __sys_next_state  = STAT_SYS_TO_START
    
    __timer_count = 0

    __mutex = RLock() 
    __stat_mutex = RLock() 
    
    @classmethod
    def add_process(cls
                        , process_name
                        , instance_id
                        , is_auto_run_on_master
                        , is_auto_run_on_slave
                        , is_exclude
                        , program_path):
        """
        Method:    add_process
        Description: 增加一个进程信息
        Parameter: 
            process_name: 进程的名称
            instance_id: 进程实例号
            is_auto_run_on_master: 在master节点上是否自动运行
            is_auto_run_on_slave: 在slave节点上是否自动运行
            is_exclude: 启动时是否是排他的
            program_path: 程序在磁盘上的路径
        Return: 
        Others: 
        """

        p = ProcessStat()
        p.set_name(process_name)
        p.set_instance_id(instance_id)
        p.set_auto_run(is_auto_run_on_master, is_auto_run_on_slave)
        p.set_exculde(is_exclude)
        p.set_program_path(program_path)

        with cls.__mutex:
            cls. __process_stat_map[process_name] = p
       
    
    @classmethod
    def set_ha_master(cls, is_only_master):
        """
        Method:    set_ha_master
        Description: 设置HA场景下，当前monitor处于主机(master)模式
        Parameter: 
                is_only_master: 当前是否没有其他在线的slave节点
        Return: 
        Others: 
        """

        with cls.__stat_mutex:
            if is_only_master is True:
                cls.__stat_ha = cls.STAT_HA_ONLY_MASTER
            else:
                cls.__stat_ha = cls.STAT_HA_MASTER

    @classmethod
    def set_ha_slave(cls):
        """
        Method:    set_ha_slave
        Description: 设置HA场景下，当前monitor处于备机(standby)模式
        Parameter: 无
        Return: 
        Others: 
        """

        with cls.__stat_mutex:
            cls.__stat_ha = cls.STAT_HA_SLAVE

    

    @classmethod
    def __is_ha_master(cls):
        """
        Method:    __is_ha_master
        Description: 判断HA场景中当前monitor是否处于主机(master)模式
        Parameter: 无
        Return: HA场景中当前monitor是否处于主机(master)模式
        Others: 
        """

        with cls.__stat_mutex:
            return cls.__stat_ha == cls.STAT_HA_MASTER



    @classmethod
    def set_sys_to_stop(cls):
        """
        Method:    set_sys_goto_stop
        Description: 设置系统即将停止
        Parameter: 无
        Return: 
        Others: 
        """

        with cls.__mutex:
            cls.__sys_next_state = cls.STAT_SYS_TO_STOP
            cls.__timer_count = 0


    @classmethod
    def set_sys_to_restart(cls):
        """
        Method:    set_sys_goto_stop
        Description: 设置系统即将重启
        Parameter: 无
        Return: 
        Others: 
        """
        
        with cls.__mutex:
            if cls.__sys_cur_state == cls.STAT_SYS_TO_START:
                cls.__sys_next_state = cls.STAT_SYS_NONE
            else:
                cls.__sys_next_state = cls.STAT_SYS_TO_RESTART
                
            cls.__timer_count = 0

    @classmethod
    def fetch_sys_next_stat(cls):
        """
        Method:    set_sys_goto_stop
        Description: 获取下一个状态
        Parameter: 无
        Return: 
        Others: 
        """
        
        with cls.__mutex:
            tmp = cls.__sys_next_state
            cls.__sys_next_state = cls.STAT_SYS_NONE

        return tmp

    @classmethod
    def __set_sys_cur_stat(cls, stat):
        """
        Method:    set_sys_goto_stop
        Description: 设置系统的状态为指定的状态
        Parameter: 
            stat: 状态
        Return: 
        Others: 
        """
        cls.__sys_cur_state = stat
        cls.__timer_count = 0

            
    @classmethod
    def check_process_stat(cls):
        """
        Method:    check_process_stat
        Description: 定时检查所有进程的状态
        Parameter: 无
        Return: 
        Others: 
        """

        with cls.__mutex:            
            for process_name, p in cls.__process_stat_map.iteritems():
                p.on_check_running()


    @classmethod
    def on_process_shakehand(cls, pid, process_name, statflag):
        """
        Method:    on_process_shakehand
        Description: 响应握手的函数
        Parameter: 
            process_name: 进程名
            statflag: 握手消息中带的状态
        Return: 
        Others: 
        """

        with cls.__mutex:            
            p = cls.__process_stat_map.get(process_name)
            if p is None:
                return

            p.on_shake_hand(pid, statflag)

    #@classmethod
    #def get_process_stat(cls):
    #    pass

    @classmethod
    def __is_app_auto_run(cls, app):
        with cls.__stat_mutex:
            if cls.__stat_ha == cls.STAT_HA_ONLY_MASTER:
                # 如果当前只有一个master节点，那么只要有一个选项是on，那么就认为需要运行
                if app.is_auto_run_on_master() or app.is_auto_run_on_slave():
                    return True
                
            elif cls.__stat_ha == cls.STAT_HA_MASTER:
                if app.is_auto_run_on_master():
                    return True

            elif cls.__stat_ha == cls.STAT_HA_SLAVE:
                if app.is_auto_run_on_slave():
                    return True

        return False

    @classmethod
    def timer_process(cls):
        cls.__timer_count += 1
        next_stat = cls.fetch_sys_next_stat()

        if next_stat == cls.STAT_SYS_TO_START or next_stat == cls.STAT_SYS_TO_RESTART:
            cls.__set_sys_cur_stat(next_stat)
                        
        elif next_stat == cls.STAT_SYS_TO_STOP:
            if cls.__sys_cur_state != cls.STAT_SYS_STOPED:
                cls.__set_sys_cur_stat(next_stat)
                
                
        if cls.__sys_cur_state == cls.STAT_SYS_TO_START:
            cls.__start_idle_process()
            cls.__set_sys_cur_stat(cls.STAT_SYS_RUNNING)
            
        elif cls.__sys_cur_state == cls.STAT_SYS_RUNNING:
            cls.__start_idle_process()

        elif cls.__sys_cur_state == cls.STAT_SYS_TO_STOP:
        
            if cls.is_all_process_stoped():
                cls.__set_sys_cur_stat(cls.STAT_SYS_STOPED)
                
            else:
                # 累计10秒左右，如果进程没有自动停止的话，就强制停止
                if cls.__timer_count > 10:
                    cls.force_stop_all_process()
                    cls.__set_sys_cur_stat(cls.STAT_SYS_STOPED)
            
        elif cls.__sys_cur_state == cls.STAT_SYS_TO_RESTART:
            
            if cls.is_all_process_stoped():
                cls.__set_sys_cur_stat(cls.STAT_SYS_TO_START)
            else:
                # 累计10秒左右，如果进程没有自动停止的话，就强制停止
                if cls.__timer_count > 10:
                    cls.force_stop_all_process()
                    cls.__set_sys_cur_stat(cls.STAT_SYS_TO_START)
            
        elif cls.__sys_cur_state == cls.STAT_SYS_STOPED:
            pass
            
        
    @classmethod
    def __start_idle_process(cls):
        """
        Method:    start_idle_process
        Description: 启动不在运行的进程
        Parameter: 无
        Return: 
        Others: 
        """

        with cls.__mutex:                               
            for process_name, p in cls.__process_stat_map.iteritems():

                # 如果进程不需要自动启动 则跳过
                if not cls.__is_app_auto_run(p):
                    continue
                
                if p.is_stopped():
                    # 启动进程
                    p.start_process()

                # 如果进程是需要独占方式启动的，那么需要等该进程启动后才能启动其他进程
                # 通常这类进程是关键进程，少了该进程整个系统无法正常运行
                if (p.is_starting() or p.is_initializing()) and p.is_exclude():
                    break

    @classmethod
    def get_shakehand_ack(cls, process_name):
        """
        Method:    get_shakehand_ack
        Description: 获取业务进程握手请求的应答消息的数据
        Parameter: 
            process_name: 进程名
        Return: 
        Others: 
        """
        with cls.__mutex:                
            p = cls.__process_stat_map.get(process_name)
            if p is None:
                return []

        if cls.__sys_cur_state in (cls.STAT_SYS_TO_STOP, cls.STAT_SYS_TO_RESTART, cls.STAT_SYS_STOPED):
            return [bf.BasicApp.SHAKEHANDACK_STOP]
        else:
            return [bf.BasicApp.SHAKEHANDACK_OK]

    @classmethod
    def is_all_process_stoped(cls):
        """
        Method:    is_all_process_stoped
        Description: 判断是否所有的进程已经停止
        Parameter: 无
        Return: 是否所有的进程已经停止
        Others: 
        """

        with cls.__mutex:
            for process_name, p in cls.__process_stat_map.iteritems():
                if not p.is_stopped():
                    return False

            return True

    @classmethod
    def force_stop_all_process(cls):
        """
        Method:    force_stop_all_process
        Description: 强制停止所有的进程
        Parameter: 无
        Return: 
        Others: 
        """

        with cls.__mutex:            
            for process_name, p in cls.__process_stat_map.iteritems():
                p.stop_process()

        tracelog.info("all process stopped.")

    @classmethod
    def get_running_process_pids(cls):
        # 获取当前正在运行的进程的pid列表
        running_pids = []
        with cls.__mutex:            
            for p in cls.__process_stat_map.itervalues():
                if not p.is_stopped():
                    running_pids.append(p.get_pid())

        return running_pids
        