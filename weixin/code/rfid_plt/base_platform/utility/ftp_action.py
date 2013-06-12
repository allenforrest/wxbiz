#coding=gbk
import ftplib 
import os.path

def upload_file(server_ip
                    , server_port
                    , username
                    , password
                    , local_file_path
                    , peer_file_path):
    """
    Method: upload_file
    Description: ͨ��FTP�ϴ��ļ�
    Parameter: 
        server_ip: FTP������IP
        server_port: FTP�������˿�
        username: �û���
        password: ����
        local_file_path: �����ļ�·��
        peer_file_path: �Զ��ļ�·��

    Return: �����룬������Ϣ
    Others: 
    """

    client = ftplib.FTP()
    ret = 0
    msg = ""
    
    try:            
        client.connect(server_ip, server_port)
        client.login(username, password)
        file_handler = open(local_file_path, "rb")        
        client.storbinary("STOR " + peer_file_path, file_handler)        
    except Exception, e:     
        ret =  -1
        msg = str(e)        

    try:
        client.quit()
    except:
        try:
            client.close()
        except:
            pass

    return ret, msg

    
