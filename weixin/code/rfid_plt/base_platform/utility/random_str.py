#coding=gbk
import random
def random_str(randomlength=28):
    """
    Function: random_str
    Description: ����ָ�����ȵ�����ַ�����������Сд��ĸ������
    Parameter: 
        randomlength: ���ɵ��ַ�������        
    Return: ���ɵ��ַ���
    Others: 
    """
    
    value = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in xrange(randomlength):
        value += chars[random.randint(0, length)]

    return value


