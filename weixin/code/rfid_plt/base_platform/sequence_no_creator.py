#coding=gbk

#��ͬ�̲߳�Ҫ����һ��SequenceNoCreator���ã����Ը���ʹ���Լ��Ķ���ʵ��
#���һ��Ҫ���ã�������̱߳���
class SequenceNoCreator():
    def __init__(self):
        self.__init_flag = False
        self.__sequence_no = None
        self.__max_no = None
        self.__min_no = None
        self.__step = None
    
    def get_new_no(self):
        if self.__init_flag is False:
            return 0
        
        self.__sequence_no += self.__step
        if self.__sequence_no >= self.__max_no:
            self.__sequence_no = self.__min_no
        return self.__sequence_no
    
    def init_creator(self, max_no, sequence_no=0, min_no=0, step=1):
        self.__init_flag = True
        self.__sequence_no = sequence_no
        self.__max_no = max_no
        self.__min_no = min_no
        self.__step = step    
        