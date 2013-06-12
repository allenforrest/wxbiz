#coding=gbk
import random
def random_str(randomlength=28):
    """
    Function: random_str
    Description: 生成指定长度的随机字符串，包含大小写字母和数字
    Parameter: 
        randomlength: 生成的字符串长度        
    Return: 生成的字符串
    Others: 
    """
    
    value = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in xrange(randomlength):
        value += chars[random.randint(0, length)]

    return value


