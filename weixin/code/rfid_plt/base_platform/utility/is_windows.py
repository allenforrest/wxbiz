#coding=gbk
import platform

def is_windows():
    """
    Function: is_windows
    Description: 判断操作系统是否windows
    Parameter:无 
    Return: 
        True,是windows
        False,不是windows
    Others: 
    """
    if platform.system().lower() == "windows":
        return True
    else:
        return False
        