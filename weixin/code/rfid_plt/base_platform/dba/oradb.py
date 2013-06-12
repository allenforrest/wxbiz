#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-22
Description: 数据库连接管理
Others:
Key Class&Method List:
    1. Connection: oracle数据库连接
    2. Query: oracle数据库操作
    3. Backup: 数据库的备份和还原
History:
1. Date:
   Author:
   Modification:
"""

import os
import subprocess
import tempfile 
import threading
import time
import uuid

# 防止oracle的错误信息是乱码
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import cx_Oracle

from .base import DBConnectionPool, DBConnection, DBQuery, DBConnectionInfo
from .error import DBConnectError, DBQueryError, DBError
from .base import ROOT_TRANS


def create_connection(conn_info):
    """
    Method: create_connection
    Description: 数据库连接创建回调函数
    """
    return Connection(conn_info)



class ConnectionInfo(DBConnectionInfo):
    """
    Class: ConnectionInfo
    Description: oracle 数据库连接信息
    """
    def __init__(self, *args, **kargs):
        """
        Method: __init__
        Description: 数据库连接信息初始化
        """
        info = {
            'dbms_type': 'oracle',
            'host': 'localhost',
            'port': 1521,
            'username': 'system',
            'password': 'Oracle-1',
            'db': None,
            'service_name': None,
            'sysdba': True
            }
            
        info.update(kargs)         
        
        DBConnectionInfo.__init__(self, *args, **info)

         
class Connection(DBConnection):
    """
    Class: OraConnection
    Description: oracle数据库连接
    Base: DBConnection
    Others:
    """

    def __init__(self, conn_info):
        DBConnection.__init__(self, conn_info)

        # 事务嵌套层次通常很少，所以直接使用list，不使用字典等
        self._trans_names = []

    def connect(self, conn_info):
        """
        Method: connect
        Description: 实现数据库的连接
        Parameters:
            1. conn_info: 数据库连接信息
        """
        user = conn_info.info['username']
        password = conn_info.info['password']
        sid = None
        service_name = None
        if 'db' in conn_info.info:
            sid = conn_info.info['db']
        if 'service_name' in conn_info.info:
            service_name = conn_info.info['service_name']
        host = conn_info.info['host']
        port = conn_info.info['port']
        kargs = {}
        
        if conn_info.info['sysdba']:
            kargs['mode'] = cx_Oracle.SYSDBA
            
        if host is None:
            self._connection = cx_Oracle.connect(user=user, password=password, dsn=sid, **kargs)
            return
            
        dsn = self._makedsn(host, port, sid, service_name = service_name)
        #print("dsn=%s (%s:%s)" % (dsn, user, password))
        
        self._connection = cx_Oracle.connect(user=user, password=password, dsn=dsn, **kargs)

    def _makedsn(self, host, port, sid, service_name = 'ORCL'):
        """
        Method: _makedsn
        Description: 生成连接字符串DSN
        Parameter: 
            host: 数据库服务器名
            port: 数据库服务器端口
            sid: 数据库名
            service_name: 数据库服务名
        Return: 
            非None: Oracle数据库连接字符串
        Others: 
        """
        if host.find(',') == -1:
            versions = cx_Oracle.version.split('.')
            if tuple(int(x) for x in versions) >= (5, 1, 1):
                if service_name is not None:
                    return cx_Oracle.makedsn(host, port, service_name = service_name)
                return cx_Oracle.makedsn(host, port, sid)
            dsn = cx_Oracle.makedsn(host, port, sid)
            if service_name is not None:
                dsn.replace('SID', 'SERVICE_NAME')
        else:
            hosts = host.split(',')
            index = 0
            address = ''
            for host in hosts:
                address += '(ADDRESS=(PROTOCOL=TCP)(HOST=%s)(PORT=%s))' % (host, port)
            rac = '(LOAD_BALANCE=ON)(FAILOVER=ON)'
            if service_name is not None:
                dsn = '(DESCRIPTION=%s(ADDRESS_LIST=%s)(CONNECT_DATA=(SERVICE_NAME=%s)))' % (rac, address, service_name)
            else:
                dsn = '(DESCRIPTION=%s(ADDRESS_LIST=%s)(CONNECT_DATA=(SID=%s)))' % (rac, address, sid)
        return dsn

    def get_query(self):
        """
        Method:    get_query
        Description: 获取一个查询接口
        Parameter: 无
        Return: DBQuery的实例
        Others:
        """

        return Query(self)

    def begin(self, name = ROOT_TRANS):
        """
        Method:    begin
        Description: 启动事务
        Parameter:
            1. name: 事务的名字
        Return:
        Others:
        """
        if name == ROOT_TRANS:
            self._connection.begin()
            return
            
        if name in self._trans_names:
            raise DBError('specified name(%s) already exists.' % name)
            
        query = self.get_query()
        query.execute('SAVEPOINT %s' % name)
        
        self._trans_names.append(name)

    def commit(self, name = ROOT_TRANS):
        """
        Method:    commit
        Description: 提交事务
        Parameter:
            1. name: 事务的名字
        Return:
        Others:
        """
        if name == ROOT_TRANS:
            self._connection.commit()
            self._trans_names = []            
            return

        
        for i, tmp_name  in enumerate(self._trans_names): 
            if tmp_name == name:
                del self._trans_names[i:]
                break
        else:
            raise DBError('specified name(%s) not found in %s.' % (name, self._trans_names))
            

    def rollback(self, name = ROOT_TRANS):
        """
        Method:    rollback
        Description: 回滚事务
        Parameter:
            1. name: 事务的名字
        Return:
        Others:
        """

        if name == ROOT_TRANS:
            self._connection.rollback()
            self._trans_names = []
            return

        for i, tmp_name  in enumerate(self._trans_names): 
            if tmp_name == name:
                self.get_query().execute('ROLLBACK TO SAVEPOINT %s' % name)        
                del self._trans_names[i:]
                break
        else:
            raise DBError('specified name(%s) not found in %s.' % (name, self._trans_names))
            
        
    
    def get_dbms_type(self):
        """
        Method:    get_dbms_type
        Description: 获取数据库系统的名称
        Parameter: 无
        Return: 数据库系统的名称
        Others:
        """

        return "oracle"

class Query(DBQuery):
    """
    Class: Query
    Description: 数据库操作类
    Base: DBQuery
    Others:
    """

    def __init__(self, connection):
        """
        Method: __init__
        Description: Query类初始化
        Parameter: 
            connection: 数据库连接
        Return: 
        Others: 
        """
        self._cursor = None
        
        DBQuery.__init__(self, connection)
        self._cursor = self._connection._connection.cursor()
    
    def select_cursor(self, sql, *args, **dw):
        """
        Method:    select
        Description: 执行select语句，返回查询结果
        Parameter:
            sql: SQL语句
            *args: 传递给数据库接口的参数
            **dw: 传递给数据库接口的参数
        Return: 查询游标
        Others:
        """

        try:
            self._cursor.execute(sql, *args, **dw)
            return self._cursor
        except Exception as e:
            raise DBQueryError(e)

    def select(self, sql, *args, **dw):
        """
        Method:    select
        Description: 执行select语句，返回查询结果
        Parameter:
            sql: SQL语句
            *args: 传递给数据库接口的参数
            **dw: 传递给数据库接口的参数
        Return: 查询结果
        Others:
        """
        records = []
        try:
            self._cursor.execute(sql, *args, **dw)
            result = self._cursor.fetchall()            
            return result
        except Exception as e:
            raise DBQueryError(e)

    def execute(self, sql, *args, **dw):
        """
        Method:    execute
        Description: 执行修改类的SQL语句
        Parameter:
            sql: SQL语句
            *args: 传递给数据库接口的参数
            **dw: 传递给数据库接口的参数
        Return:
        Others:
        """
        try:
            self._cursor.execute(sql, *args, **dw)
            return self._cursor
        except Exception as e:
            raise DBQueryError(e)

    def executemany(self, sql, seq_of_parameters):
        """
        Method:    executemany
        Description: 批量执行SQL
        Parameter:
            sql: SQL语句
            seq_of_parameters: 与SQL语句配套的序列
        Return:
        Others:
        """
        try:
            self._cursor.executemany(sql, seq_of_parameters)
        except Exception as e:
            raise DBQueryError(e)

    def executescript(self, sql_script):
        """
        Method:    executescript
        Description: 执行一段SQL脚本
        Parameter:
            sql_script: 一段SQL脚本
        Return:
        Others:
        """
        sql_commands = sql_script.split(';')
        try:
            for sql in sql_commands:
                self.execute(sql)
        except Exception as e:
            raise DBQueryError(e)

    def close(self):
        """
        Method:    close
        Description: 关闭当前查询
        Parameter:
        Return:
        Others:
        """
        if self._cursor is not None:
            try:
                self._cursor.close()
            except:
                # errors will be ignored.
                pass
            self._cursor = None

class Backup():
    __backupset = {'database': {'pattern': '%d_t%t_s%s_p%p.bak', 'compress': True},
                  'archivelog all': {'pattern': '%d_t%t_s%s_p%p.arch', 'compress': True},
                  'current controlfile': {'pattern': '%d_t%t_s%s_p%p.ctl', 'compress': False}}
    """
    Class: Backup
    Description: 数据库的备份和还原
    Base: 
    Others: 
    """
    def __init__(self, conn_info):
        self._conn_info = conn_info
        self._connection = None
        self._query = None

    def open(self):
        """
        Description: 打开RMAN管道连接
        Parameters:
        """
        conn_info = self._conn_info
        connectionPool = DBConnectionPool(conn_info)
        self._connection = connectionPool.get_connection()
        self._query = self._connection.get_query()

    def show_configure(self):
        """
        Method: show_configure
        Description: 显示RMAN配置
        Parameter: 无
        Return: 
        Others: 
        """
        self.send_command("SHOW ALL")

    def backup(self, backup_dir = None, incremental = False, level = 0, compress = True):
        """
        Description: 备份数据库
        Parameters:
            1. backup_dir: 备份路径
            2. incremental: 是否增量备份
            3. level: 增量备份的级别
            4. compress: 是否压缩
        Return:
            返回备份文件所在的目录
        Others:
            在做增量备份的时候，必须创建0级备份
        """
        backup_time = time.strftime('%Y%m%d-%H%M%S')
        try:
            self.open()
            command = "BACKUP"
            save_folder = os.path.join(backup_dir, 'backupset')
            for backup in self.__backupset:
                rman_command = command
                if compress is True and self.__backupset[backup]['compress'] is True:
                    rman_command = command + " AS COMPRESSED BACKUPSET"
                pattern = self.__backupset[backup]['pattern']
                if incremental == True:
                    rman_command = rman_command + (" INCREMENTAL LEVEL=%d DATABASE" % level)
                    backup_folder = os.path.join(save_folder, 'incremental')
                else:
                    rman_command = rman_command + " %s " % backup
                    backup_folder = os.path.join(save_folder, 'full')
                backup_folder = os.path.join(backup_folder, backup_time)
                if backup_folder.startswith('+'):
                    diskgroup = backup_folder.split('/')[0][1:]
                    #sql = "ALTER DISKGROUP %s ADD DIRECTORY '%s'" % (diskgroup, save_folder)
                    #self._query.execute(sql)
                elif not os.path.exists(backup_folder):
                    os.makedirs(backup_folder)
                backup_file = os.path.join(backup_folder, pattern)
                rman_command = rman_command + ' FORMAT=\'%s\'' % backup_file
                self.send_command(rman_command)
        finally:
            self.close()
        return backup_folder

    def _get_backup_files(self, backupset_folder):
        """
        Method: _get_backup_files
        Description: 得到数据库备份文件列表
        Parameter:
            backupset_folder: 备份集目录
        Return:
        Others:
        """
        if not os.path.exists(backupset_folder):
            raise Exception("backup folder '%s' does not exist." % backupset_folder)
        if not os.path.isdir(backupset_folder):
            raise Exception("backup folder '%s' is not a directory." % backupset_folder)
        backup_files = os.listdir(backupset_folder)
        backupset_ctl = None
        backupset_bak = None
        for backup_file in backup_files:
            if backup_file[-4:].lower() == '.ctl':
                backupset_ctl = os.path.join(backupset_folder, backup_file)
            elif backup_file[-4:].lower() == '.bak':
                backupset_bak = backupset_folder
        if backupset_ctl is None or backupset_bak is None:
            raise Exception('backup folder was lack of data file or control file.')
        return (backupset_ctl, backupset_bak)

    def restore(self, backupset_source):
        """
        Method: restore
        Description: 还原数据库
        Parameter:
            backupset_source: 备份文件来源
        Return: 
        Others: 
        """
        if isinstance(backupset_source, tuple):
            (backupset_ctl, backupset_bak) = backupset_source
        elif os.path.isdir(backupset_source):
            (backupset_ctl, backupset_bak) = self._get_backup_files(backupset_source)
        else:
            raise Exception('backupset source is unknown.')
        try:
            self.open()
        except:
            # restore, even though database cannot be opened
            print("WARNING: database cannot be opened.")
        finally:
            self.close()
        command = "SHUTDOWN IMMEDIATE;\r\n"
        command = command + "STARTUP NOMOUNT;\r\n"
        command = command + "RESTORE CONTROLFILE FROM '%s';\r\n" % backupset_ctl
        command = command + "ALTER DATABASE MOUNT;\r\n"
        command = command + "CATALOG START WITH '%s' NOPROMPT;\r\n" % backupset_bak;
        command = command + "RESTORE DATABASE;\r\n"
        command = command + "RECOVER DATABASE;\r\n"
        command = command + "alter database open resetlogs"
        try:
            self.send_command(command, False)
        except:
            self.send_command('STARTUP MOUNT FORCE', False)

    def close(self):
        """
        Method: close
        Description: 关闭RMAN连接
        Parameter: 无
        Return: 
        Others: 
        """
        if self._query is not None:
            self._query.close()
            self._query = None
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def _write_file(self, filename, content):
        """
        Method: write_file
        Description: 把内容写入文件,原来的内容会被覆盖
        Parameter: 
            filename: 文件名
            content: 文件内容
        Return: 
        Others: 
        """
        f = None
        try:
            f = open(filename, mode="w")
            for line in content:
                if line != None: f.write(line)
        except IOError as e:
            print('WriteError: %s' % e)
            raise e
        finally:
            if f != None: f.close

    def exec_shell_command(self, args, stdin = None, ignore = False, exec_user = None):
        """
        Method: exec_shell_command
        Description: 调用系统命令，返回执行结果和退出码
        Parameters:
            stdin: 标准输入
            ignore: 是否忽视错误，作为退出码返回
            exec_user: 执行用户
        Return: (return_code, output, error)
            return_code: 退出码
            output: 程序执行的输出内容
            error: 程序执行的错误内容
        Others:
        """
        if exec_user != None:
            args = 'su %s -c "%s"' % (exec_user, args.replace('"', '\\"'))
        print(args)
        if stdin == None:
            p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
        else:
            p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE);
            p.stdin.write(stdin)
        output = [];
        error = []
        while True:
            line = p.stdout.readline()
            line = line.strip()
            if line == '' and p.poll() is not None:
                break;
            if line != '':
                print(line)
                output.append(line)
            p.stdout.flush()
        return_code = p.returncode;
        if return_code != 0:
            error = self.read_from_std(p.stderr)
            if not ignore: raise OSError("[ErrorCode=%d] %s" % (return_code, error))
        return (return_code, output, error)

    def read_from_std(self, std):
        """
        Method: read_from_std
        Description: 读取输入输出内容
        Parameters:
            std: 标准输入输出
        Return:
            None: 无法读取内容
            非None: 成功读取内容
        """
        result = []
        for line in std:
            result.append(line.strip())
        return result
    
    def send_command(self, command, is_backup = True):
        """
        Method: send_command
        Description: 发送命令到RMAN管道
        Parameter: 
            command: 关闭RMAN连接
            is_backup: 是否是备份
        Return: 
        Others: 
        """
        if self._query is None and is_backup is True:
            return
        cmdfile = tempfile.NamedTemporaryFile()
        cmdfilename = cmdfile.name

        self._write_file(cmdfilename, 'RUN{\r\n%s;\r\n}' % command)
        sysdba_user = self._conn_info.info['username']
        sysdba_pass = self._conn_info.info['password']
        if 'db' in self._conn_info.info:
            service_name = self._conn_info.info['db']
        elif 'service_name' in self._conn_info.info:
            service_name = self._conn_info.info['service_name']
        if is_backup is True:
            cmd = 'rman TARGET %s/%s@%s NOCATALOG CMDFILE "%s"' % (sysdba_user, sysdba_pass, service_name, cmdfilename)
        else:
            cmd = 'export ORACLE_SID=%s;rman TARGET / NOCATALOG CMDFILE "%s"' % (service_name, cmdfilename)
        self.exec_shell_command(cmd)
