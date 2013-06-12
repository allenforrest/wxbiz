/*CREATE DATABASE testdb 
    MAXINSTANCES 1
    MAXLOGHISTORY 1
    MAXLOGFILES 5
    MAXLOGMEMBERS 5
    MAXDATAFILES 100
    DATAFILE '/opt/11g/oracle/oradata/testdb/system.dbf' size 100M
    UNDO TABLESPACE undotbs DATAFILE '/opt/11g/oracle/oradata/testdb/undotbs.dbf' size 50M
    AUTOEXTEND ON NEXT 5120K MAXSIZE UNLIMITED
    DEFAULT TEMPORARY TABLESPACE tempts
    CHARACTER SET ZHS16GBK
    NATIONAL CHARACTER SET AL16UTF16
    SYSAUX DATAFILE '/opt/11g/oracle/oradata/testdb/sysaux01.dbf' SIZE 100M reuse autoextend on next 10m maxsize unlimited    
    LOGFILE GROUP 1 ('/opt/11g/oracle/oradata/testdb/redo01.log') size 100M,        
            GROUP 2 ('/opt/11g/oracle/oradata/testdb/redo02.log') size 100M,        
            GROUP 3 ('/opt/11g/oracle/oradata/testdb/redo03.log') size 100M; 
            

*/


-- 当表空间存在时，drop掉
create or replace procedure proc_drop_tablespace( 
    p_tablespace_name in varchar2 
) is 
    v_count number(10); 
begin 
   select count(*) 
   into v_count 
   from dba_tablespaces 
   where tablespace_name= upper(p_tablespace_name); 

   if v_count > 0 then 
      execute immediate 'drop tablespace ' || p_tablespace_name ||' including contents and datafiles'; 
   end if; 
end proc_drop_tablespace; 

/

-- 删除用户
create or replace procedure proc_drop_user( 
    p_user_name in varchar2 
) is 
    v_count number(10); 
begin 
   select count(*) 
   into v_count 
   from dba_users 
   where username = upper(p_user_name) or username = p_user_name; 

   if v_count > 0 then 
      execute immediate 'drop user ' || p_user_name ||' cascade'; 
   end if; 
end proc_drop_user; 

/

-- 删除profile
create or replace procedure proc_drop_profile( 
    p_profile_name in varchar2 
) is 
    v_count number(10); 
begin 
   select count(*) 
   into v_count 
   from dba_profiles 
   where profile = upper(p_profile_name) or profile = p_profile_name; 

   if v_count > 0 then 
      execute immediate 'drop profile ' || p_profile_name ||' cascade'; 
   end if; 
end proc_drop_profile; 

/

-- 当数据表存在时，drop掉(为用户user_acp创建的)
-- 当数据表存在时，drop掉(为用户user_acp创建的)
create or replace procedure proc_drop_table( 
    p_table_name in varchar2 
) is 
    v_count number(10); 
begin 
   select count(*) 
   into v_count 
   from all_tables  -- 不使用user_tables，否则其他用户调用该存储过程就找不到记录
   where owner = upper(user) and  table_name = upper(p_table_name) or table_name = p_table_name; 

   if v_count > 0 then 
      execute immediate 'drop table ' || user || '.' || p_table_name ||' purge'; 
   end if; 
end proc_drop_table; 

/


-- 创建表空间
--drop tablespace plt including contents and datafiles;
exec proc_drop_tablespace('tblsp_acp');
create tablespace tblsp_acp 
    DATAFILE '/opt/11g/oracle/oradata/orcl/tblsp_acp_01.dbf' SIZE 100M REUSE AUTOEXTEND ON next 100M  maxsize unlimited;

-- 取消密码过期的限制，否则就会到期后程序无法正常运行
exec proc_drop_profile('profile_acp');
create profile profile_acp limit
 FAILED_LOGIN_ATTEMPTS  10  --指定锁定用户的登录失败次数
 PASSWORD_LOCK_TIME 0.002     --指定用户被锁定天数(约3分钟）
 PASSWORD_LIFE_TIME unlimited    --指定口令可用天数
 IDLE_TIME unlimited
 CONNECT_TIME unlimited;
 
exec proc_drop_user('user_acp');
create user user_acp 
  identified by user_acp 
  default tablespace tblsp_acp
  profile profile_acp;
  
grant connect, resource to user_acp; 
grant create tablespace, drop tablespace to user_acp; 
grant create view to user_acp; 
grant all on proc_drop_table to user_acp;


exec proc_drop_user('user_sync');
create user user_sync 
  identified by user_sync 
  default tablespace tblsp_acp
  profile profile_acp;
  
grant connect, resource to user_sync; 
grant create tablespace, drop tablespace to user_sync; 
grant create view to user_sync; 
grant all on proc_drop_table to user_sync;



