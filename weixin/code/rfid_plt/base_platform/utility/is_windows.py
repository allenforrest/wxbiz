#coding=gbk
import platform

def is_windows():
    """
    Function: is_windows
    Description: �жϲ���ϵͳ�Ƿ�windows
    Parameter:�� 
    Return: 
        True,��windows
        False,����windows
    Others: 
    """
    if platform.system().lower() == "windows":
        return True
    else:
        return False
        