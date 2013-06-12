#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-19
Description: ������ʵ���˽���״̬������
Others:      
Key Class&Method List: 
             1. ProcessStat: �������̵�״̬
             2. ProcessStatMgr: ����״̬������
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
    Description: �������̵�״̬
    Base: 
    Others: 
    """

    STAT_PROCESS_STARTING       = 0  # ��������(monitor��ʼ����ĳ������)
    STAT_PROCESS_INITIALIZING   = 1  # ���ڳ�ʼ��
    STAT_PROCESS_RUNNING        = 2  # ����������
    STAT_PROCESS_STOPPING       = 3  # ����ֹͣ
    STAT_PROCESS_STOPPED        = 4  # �Ѿ�ֹͣ
    
    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
        """

        # ���̵�pid���ڽ���������ͨ��������Ϣ�õ����̵�pid
        self.__pid = bf.INVALID_PID

        # ���̵�����
        self.__process_name = ""
        
        # ���̵�ʵ���ţ���ϵͳ�ڶ�ʵ���ı��
        self.__instance_id = 0

        # ��ǰ������״̬
        self.__cur_stat = ProcessStat.STAT_PROCESS_STOPPED

        # ����ʱ���Ƿ���Ҫ��ռ��һ��ʱ��
        # �Ա���������������̣���������������
        self.__start_excluded = False  

        # �Ƿ��Զ�����
        self.__auto_run_on_master = True
        self.__auto_run_on_slave = True

        # �����ڴ����ϵ�λ��
        self.__program_path = ""

        # ���ּ�����
        self.__shake_hand = 0

        # subprocess.Popen��ʵ��
        self.__popen_inst = None

    def get_pid(self):
        return self.__pid
        
    def set_name(self, name):
        """
        Method:    set_name
        Description: ���ý��̵�����
        Parameter: 
            name: ���̵�����
        Return: 
        Others: 
        """

        self.__process_name = name

    def get_name(self):
        """
        Method:    get_name
        Description: ��ȡ���̵�����
        Parameter: ��
        Return: ���̵�����
        Others: 
        """

        return self.__process_name
    
    def set_instance_id(self, instance_id):
        """
        Method:    set_instance_id
        Description: ���ý��̵�ʵ����
        Parameter: 
            name: ���̵�ʵ����
        Return: 
        Others: 
        """

        self.__instance_id = instance_id

    def get_instance_id(self):
        """
        Method:    get_name
        Description: ��ȡ���̵�ʵ����
        Parameter: ��
        Return: ���̵�ʵ����
        Others: 
        """

        return self.__instance_id

    def set_starting(self):
        """
        Method:    set_starting
        Description: ���ý��̵�״̬Ϊ����������
        Parameter: ��
        Return: 
        Others: 
        """

        self.__cur_stat = ProcessStat.STAT_PROCESS_STARTING
        
    def is_starting(self):
        """
        Method:    is_starting
        Description: �жϽ����Ƿ�����������
        Parameter: ��
        Return: �����Ƿ�����������
        Others: 
        """

        return self.__cur_stat == ProcessStat.STAT_PROCESS_STARTING

    def set_initializing(self):
        """
        Method:    set_initializing
        Description: ���ý��̵�״̬Ϊ���ڳ�ʼ����
        Parameter: ��
        Return: ���̵�״̬Ϊ���ڳ�ʼ����
        Others: 
        """

        self.__cur_stat = ProcessStat.STAT_PROCESS_INITIALIZING
    
    def is_initializing(self):
        """
        Method:    is_initializing
        Description: �жϽ����Ƿ����ڳ�ʼ��
        Parameter: ��
        Return: �����Ƿ����ڳ�ʼ��
        Others: 
        """

        return self.__cur_stat == ProcessStat.STAT_PROCESS_INITIALIZING

    def set_running(self):
        """
        Method:    set_running
        Description: ���ý���Ϊ����������
        Parameter: ��
        Return: 
        Others: 
        """

        self.__cur_stat = ProcessStat.STAT_PROCESS_RUNNING
        
    def is_running(self):
        """
        Method:    is_running
        Description: �жϽ����Ƿ�����������
        Parameter: ��
        Return: �����Ƿ�����������
        Others: 
        """

        return self.__cur_stat == ProcessStat.STAT_PROCESS_RUNNING

    def set_stopping(self):
        """
        Method:    set_stopping
        Description: ���ý��̵�״̬Ϊ����ֹͣ
        Parameter: ��
        Return: 
        Others: 
        """

        self.__cur_stat = ProcessStat.STAT_PROCESS_STOPPING
        
    def is_stopping(self):
        """
        Method:    is_stopping
        Description: �жϽ��̵�״̬�Ƿ�Ϊ����ֹͣ
        Parameter: ��
        Return: 
        Others: 
        """

        return self.__cur_stat == ProcessStat.STAT_PROCESS_STOPPING

    def __set_stoped(self):
        """
        Method:    __set_stoped
        Description: ���ý��̵�״̬Ϊ�Ѿ�ֹͣ
        Parameter: ��
        Return: 
        Others: 
        """

        self.__cur_stat = ProcessStat.STAT_PROCESS_STOPPED

    def is_stopped(self):
        """
        Method:    is_stopped
        Description: �жϽ��̵�״̬�Ƿ�Ϊ�Ѿ�ֹͣ
        Parameter: ��
        Return: 
        Others: 
        """

        return self.__cur_stat == ProcessStat.STAT_PROCESS_STOPPED

    
    def set_exculde(self, is_exclude):
        """
        Method:    set_exculde
        Description: ���ý�������ʱ�Ƿ���������
        Parameter: 
            is_exclude: ����ֵ, ��������ʱ�Ƿ���������
        Return: 
        Others: 
        """

        self.__start_excluded = is_exclude
        
    def is_exclude(self):
        """
        Method:    is_exclude
        Description: �жϽ�������ʱ�Ƿ���������
        Parameter: ��
        Return: 
        Others: 
        """

        return self.__start_excluded

    def set_auto_run(self, is_auto_run_on_master, is_auto_run_on_slave):
        """
        Method:    set_auto_run
        Description: ���ý����Ƿ����Զ������е�
        Parameter: 
            is_auto_run_on_master: ����ֵ��������master���Ƿ����Զ������е�
            is_auto_run_on_slave: ����ֵ��������slave���Ƿ����Զ������е�
        Return: 
        Others: 
        """

        self.__auto_run_on_master = is_auto_run_on_master
        self.__auto_run_on_slave = is_auto_run_on_slave
        
    def is_auto_run_on_master(self):
        """
        Method:    is_auto_run_on_master
        Description: �жϽ�����master���Ƿ����Զ������е�
        Parameter: ��
        Return: �����Ƿ����Զ������е�
        Others: 
        """

        return self.__auto_run_on_master

    def is_auto_run_on_slave(self):
        """
        Method:    is_auto_run_on_slave
        Description: �жϽ�����slave���Ƿ����Զ������е�
        Parameter: ��
        Return: �����Ƿ����Զ������е�
        Others: 
        """

        return self.__auto_run_on_slave


    def set_program_path(self, program_path):
        """
        Method:    set_program_path
        Description: ������������ڴ����ϵ�·��
        Parameter: 
            program_path: ��������ڴ����ϵ�·��
        Return: 
        Others: 
        """

        self.__program_path = program_path


    def get_program_path(self):
        """
        Method:    get_program_path
        Description: ��ȡ��������ڴ����ϵ�·��
        Parameter: ��
        Return: ��������ڴ����ϵ�·��
        Others: 
        """

        return self.__program_path
        

    def on_shake_hand(self, pid, statflag):
        """
        Method:    on_shake_hand
        Description: ��monitor�յ�������Ϣ�����Ӧ����
        Parameter: 
            statflag: ������Ϣ�д���״̬���
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
        Description: ��Ӧ��ʱ�˲����״̬�ĺ���
        Parameter: ��
        Return: 
        Others: 
        """

        if self.is_stopped():
            return
        
        # ����������Զ������ģ���ôself.__popen_inst��ΪNone��
        # ����ͨ��self.__popen_inst׼ȷ�жϽ����Ƿ��˳���
        if (self.__popen_inst is not None 
            and self.__popen_inst.poll() is not None):
            
            self.stop_process()
            return
            
        
        self.__shake_hand += 1

        # �����������������ô�������һ��ʱ��δ������������״̬Ϊֹͣ
        if self.is_starting() and self.__shake_hand >= PROCESS_STARTING_TIMEOUT:
            tracelog.info("process(%s) start timeout." % self.__process_name)
            self.stop_process()
            return

        # ����ڳ�ʼ���ڼ䣬����һ����ʱ�䣬������Ϊֹͣ
        if self.is_initializing() and self.__shake_hand >= PROCESS_INITIALIZING_TIMEOUT:
            tracelog.info("process(%s) initialize timeout." % self.__process_name)
            self.stop_process()
            return
                
        # �������ڼ䣬�������һ��ʱ�䣬������״̬Ϊֹͣ
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
        Description: ��������
        Parameter: ��
        Return: 
        Others: 
        """
        program_path = self.__program_path
        if not os.path.exists(program_path):
            # py�����ڣ���ô��ʹ��pyc
            if program_path.endswith(".py") and os.path.exists(program_path + "c"):
                program_path +="c" 
            else:
                tracelog.error("program does not exist! program_path:%s"% self.__program_path)
                return 
                
        self.stop_process()       

        try:       
            # ע��: close_fds��������ΪTrue�������ӽ��̻�̳и����̵��ļ���������¸��������ļ��޷�������������ɾ��
            # ����log�ļ�
            # ��windows��stdin��stdout��stderr���벻���ã�����close_fds�޷�����ΪTrue
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
                            
        self.set_starting() # ����״̬Ϊ ����������
        

        
    def stop_process(self):
        """
        Method:    stop_process
        Description: ֹͣ����
        Parameter: ��
        Return: 
        Others: 
        """

        if self.__popen_inst is None:
            self.__set_stoped()            
            return

        try:   
            r = self.__popen_inst.poll()
            
            if r is None: # ��������, �ȳ������Źر�
                self.__popen_inst.terminate()

                # �ȴ�10��
                for i in xrange(20):
                    r = self.__popen_inst.poll()
                    if r is not None:
                        tracelog.info("process(%s, %d) is terminated." % (self.__process_name, self.__popen_inst.pid))
                        break

                    time.sleep(0.5)
                else:
                    self.__popen_inst.kill()  # kill����
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
    Description: ����״̬������
    Base: 
    Others: 
    """

    STAT_HA_MASTER = 0      # ��ǰ��master�����������õ�slave
    STAT_HA_SLAVE = 1       # ��ǰ��slave
    STAT_HA_ONLY_MASTER = 2 # ��ǰ��master��û���������õ�slave

    STAT_SYS_TO_START   = 0 # �ȴ�����
    STAT_SYS_RUNNING    = 1 # ��������
    STAT_SYS_TO_STOP    = 2 # �ȴ�ֹͣ
    STAT_SYS_TO_RESTART = 3 # �ȴ�����
    STAT_SYS_STOPED     = 4 # �Ѿ�ֹͣ
    
    STAT_SYS_NONE       = 5 # ��״̬
    
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
        Description: ����һ��������Ϣ
        Parameter: 
            process_name: ���̵�����
            instance_id: ����ʵ����
            is_auto_run_on_master: ��master�ڵ����Ƿ��Զ�����
            is_auto_run_on_slave: ��slave�ڵ����Ƿ��Զ�����
            is_exclude: ����ʱ�Ƿ���������
            program_path: �����ڴ����ϵ�·��
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
        Description: ����HA�����£���ǰmonitor��������(master)ģʽ
        Parameter: 
                is_only_master: ��ǰ�Ƿ�û���������ߵ�slave�ڵ�
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
        Description: ����HA�����£���ǰmonitor���ڱ���(standby)ģʽ
        Parameter: ��
        Return: 
        Others: 
        """

        with cls.__stat_mutex:
            cls.__stat_ha = cls.STAT_HA_SLAVE

    

    @classmethod
    def __is_ha_master(cls):
        """
        Method:    __is_ha_master
        Description: �ж�HA�����е�ǰmonitor�Ƿ�������(master)ģʽ
        Parameter: ��
        Return: HA�����е�ǰmonitor�Ƿ�������(master)ģʽ
        Others: 
        """

        with cls.__stat_mutex:
            return cls.__stat_ha == cls.STAT_HA_MASTER



    @classmethod
    def set_sys_to_stop(cls):
        """
        Method:    set_sys_goto_stop
        Description: ����ϵͳ����ֹͣ
        Parameter: ��
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
        Description: ����ϵͳ��������
        Parameter: ��
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
        Description: ��ȡ��һ��״̬
        Parameter: ��
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
        Description: ����ϵͳ��״̬Ϊָ����״̬
        Parameter: 
            stat: ״̬
        Return: 
        Others: 
        """
        cls.__sys_cur_state = stat
        cls.__timer_count = 0

            
    @classmethod
    def check_process_stat(cls):
        """
        Method:    check_process_stat
        Description: ��ʱ������н��̵�״̬
        Parameter: ��
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
        Description: ��Ӧ���ֵĺ���
        Parameter: 
            process_name: ������
            statflag: ������Ϣ�д���״̬
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
                # �����ǰֻ��һ��master�ڵ㣬��ôֻҪ��һ��ѡ����on����ô����Ϊ��Ҫ����
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
                # �ۼ�10�����ң��������û���Զ�ֹͣ�Ļ�����ǿ��ֹͣ
                if cls.__timer_count > 10:
                    cls.force_stop_all_process()
                    cls.__set_sys_cur_stat(cls.STAT_SYS_STOPED)
            
        elif cls.__sys_cur_state == cls.STAT_SYS_TO_RESTART:
            
            if cls.is_all_process_stoped():
                cls.__set_sys_cur_stat(cls.STAT_SYS_TO_START)
            else:
                # �ۼ�10�����ң��������û���Զ�ֹͣ�Ļ�����ǿ��ֹͣ
                if cls.__timer_count > 10:
                    cls.force_stop_all_process()
                    cls.__set_sys_cur_stat(cls.STAT_SYS_TO_START)
            
        elif cls.__sys_cur_state == cls.STAT_SYS_STOPED:
            pass
            
        
    @classmethod
    def __start_idle_process(cls):
        """
        Method:    start_idle_process
        Description: �����������еĽ���
        Parameter: ��
        Return: 
        Others: 
        """

        with cls.__mutex:                               
            for process_name, p in cls.__process_stat_map.iteritems():

                # ������̲���Ҫ�Զ����� ������
                if not cls.__is_app_auto_run(p):
                    continue
                
                if p.is_stopped():
                    # ��������
                    p.start_process()

                # �����������Ҫ��ռ��ʽ�����ģ���ô��Ҫ�ȸý������������������������
                # ͨ����������ǹؼ����̣����˸ý�������ϵͳ�޷���������
                if (p.is_starting() or p.is_initializing()) and p.is_exclude():
                    break

    @classmethod
    def get_shakehand_ack(cls, process_name):
        """
        Method:    get_shakehand_ack
        Description: ��ȡҵ��������������Ӧ����Ϣ������
        Parameter: 
            process_name: ������
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
        Description: �ж��Ƿ����еĽ����Ѿ�ֹͣ
        Parameter: ��
        Return: �Ƿ����еĽ����Ѿ�ֹͣ
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
        Description: ǿ��ֹͣ���еĽ���
        Parameter: ��
        Return: 
        Others: 
        """

        with cls.__mutex:            
            for process_name, p in cls.__process_stat_map.iteritems():
                p.stop_process()

        tracelog.info("all process stopped.")

    @classmethod
    def get_running_process_pids(cls):
        # ��ȡ��ǰ�������еĽ��̵�pid�б�
        running_pids = []
        with cls.__mutex:            
            for p in cls.__process_stat_map.itervalues():
                if not p.is_stopped():
                    running_pids.append(p.get_pid())

        return running_pids
        