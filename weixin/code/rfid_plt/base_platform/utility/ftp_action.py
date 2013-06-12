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
    Description: 通过FTP上传文件
    Parameter: 
        server_ip: FTP服务器IP
        server_port: FTP服务器端口
        username: 用户名
        password: 密码
        local_file_path: 本地文件路径
        peer_file_path: 对端文件路径

    Return: 错误码，错误信息
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

    
