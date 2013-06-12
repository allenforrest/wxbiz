#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-12
Description: ���л��ͷ����л��࣬�ṩ�����ֱ��뷽ʽ: Json��Bson
             ����ͨ���̳�JsonSerializableObj��BsonSerializableObj���Զ������ݽṹ
Others:      
Key Class&Method List: 
             1. SerializableObj: JsonSerializableObj��BsonSerializableObj�Ļ���
             2. JsonSerializableObj: Json��ʽ��������л��������л���
             3. BsonSerializableObj: Bson��ʽ��������л��������л���


ע: 
 1) Ŀǰû�в���cPickle����Ҫ��Ϊ�����ݸ�ʽ�����գ����ݸ�ʽ��ͨ��
 2) ����Ϊtype_def.TYPE_STRING�����ԣ��� [type_def.TYPE_STRING]�����ԣ������ڷ����л�ʱ����unicode�Զ�ת��Ϊ��ͨ��string
    ��������µ��ַ����������л�����Ȼ��unicode�������ֵ����͵����ԣ���key����unicode



����:

class BsonStudent(BsonSerializableObj):
    
    __ATTR_DEF__ = {
                      "name":type_def.TYPE_STRING
                    , "age": type_def.TYPE_UCHAR
                    }                     

    def __cmp__(self, other):


        return cmp(self.name, other.name) or cmp(self.age, other.age)


class BsonScores(BsonSerializableObj):

    
    __ATTR_DEF__ = {                      
                     "min_scroe": type_def.TYPE_INT32
                    , "max_scroe": type_def.TYPE_INT32
                    , "avg_scroe": type_def.TYPE_FLOAT
                    , "all_scroe" : []
                    , "all_students" : [BsonStudent]
                    , "best_student" : BsonStudent
                    , "other_infos1" : {}
                    , "other_infos2" : [type_def.TYPE_STRING]
                    , "other_infos3" : type_def.TYPE_BINARY
                    }
                    
History: 
1. Date:
   Author:
   Modification:
"""


import inspect
import json
import type_def
import bson

import collections





class SerializableObj:
    """
    Class: SerializableObj
    Description: JsonSerializableObj��BsonSerializableObj�Ļ���
    Base: 
    Others: 
    """

    
    __ATTR_DEF__ = None
    
    def __init__(self):
        pass


    def init_all_attr(self):
        """
        Method:    init_all_attr
        Description: ����__ATTR_DEF__�ж�����������ƣ��Զ��������е����ԣ�����ֵΪNone
        Parameter: ��
        Return: 
        Others: 
        """

        for attr_name in self.__ATTR_DEF__.iterkeys():
            setattr(self, attr_name, None)

    def __repr__(self):    
        values = []
        for attr_name in self.__ATTR_DEF__.iterkeys():
            attr_value = getattr(self, attr_name)
            values.append("%s:%r" % (attr_name, attr_value))

        return "%s{%s}" % (self.__class__.__name__, ",".join(values))
		
    def to_ordered_dict(self):
        """
        Method:    to_ordered_dict
        Description: ���ݶ�����������ԣ�����bson��json�ܹ�ʹ�õ��ֵ�
        Parameter: ��
        Return: ��������������ֵ���ֵ�
        Others: ����Ҳ���������л��������͵�
        """

        attr_defs = self.__ATTR_DEF__

        dict_list = []
        index = 0
        for attr_name, attr_type in attr_defs.iteritems():
            v = getattr(self, attr_name)
            index += 1
            
            if v is None:
                #dict_value[attr_name] = v
                dict_list.insert(index, (attr_name, v))
                continue
                
            if type_def.TYPE_STRING <= attr_type <= type_def.TYPE_FLOAT:
                #dict_value[attr_name] = v
                dict_list.insert(index, (attr_name, v))
                continue            
            
            if attr_type == type_def.TYPE_BINARY:
                #dict_value[attr_name] = self._gen_bin_value(attr_name, v)
                dict_list.insert(index, (attr_name, self._gen_bin_value(attr_name, v)))
                continue
                
            if isinstance(attr_type, dict):
                #dict_value[attr_name] = v
                dict_list.insert(index, (attr_name, v))
                continue

            if isinstance(attr_type, list):
                #  �յ�list����ʾ��������ݲ��ù���
                if len(attr_type) == 0:
                    #dict_value[attr_name] = v
                    dict_list.insert(index, (attr_name, v))
                    continue

                item_type = attr_type[0]
                
                # list����������ݣ���serializable_obj����������
                if inspect.isclass(item_type) and issubclass(item_type, SerializableObj):                     
                    tmp = [item.to_dict() if item is not None else None for item in v]
                    #dict_value[attr_name] = tmp
                    dict_list.insert(index, (attr_name, tmp))
                    continue

                # ��������������κδ���
                #dict_value[attr_name] = v
                dict_list.insert(index, (attr_name, v))
                continue

            # ���ֻʣ��serializable_obj���������������� 
            #dict_value[attr_name] = v.to_dict()
            dict_list.insert(index, (attr_name, v.to_ordered_dict()))

        dict_value = collections.OrderedDict(dict_list)
        return dict_value
         

    def to_dict(self):
        """
        Method:    to_dict
        Description: ���ݶ�����������ԣ�����bson��json�ܹ�ʹ�õ��ֵ�
        Parameter: ��
        Return: ��������������ֵ���ֵ�
        Others: ����Ҳ���������л��������͵�
        """

        attr_defs = self.__ATTR_DEF__
        dict_value = {}

        
        for attr_name, attr_type in attr_defs.iteritems():
            v = getattr(self, attr_name)

            if v is None:
                dict_value[attr_name] = v
                continue
                
            if type_def.TYPE_STRING <= attr_type <= type_def.TYPE_FLOAT:
                dict_value[attr_name] = v
                continue            
            
            if attr_type == type_def.TYPE_BINARY:
                dict_value[attr_name] = self._gen_bin_value(attr_name, v)
                continue
                
            if isinstance(attr_type, dict):
                dict_value[attr_name] = v
                continue

            if isinstance(attr_type, list):
                #  �յ�list����ʾ��������ݲ��ù���
                if len(attr_type) == 0:
                    dict_value[attr_name] = v
                    continue

                item_type = attr_type[0]
                
                # list����������ݣ���serializable_obj����������
                if inspect.isclass(item_type) and issubclass(item_type, SerializableObj):                     
                    tmp = [item.to_dict() if item is not None else None for item in v]
                    dict_value[attr_name] = tmp
                    continue

                # ��������������κδ���
                dict_value[attr_name] = v
                continue

            # ���ֻʣ��serializable_obj���������������� 
            dict_value[attr_name] = v.to_dict()

        return dict_value

    @classmethod
    def from_dict(cls, dict_value):
        """
        Method:    from_dict
        Description: �����ֵ䣬���ɵ�����ʵ���������Ե�ֵ�����ֵ���ͬ��key��Ӧ��ֵ
        Parameter: 
            dict_value: �ֵ䣬�����˶���ʵ��������ֵ
        Return: ����ʵ��
        Others: 
        """

        if dict_value is None:
            return None
            
        attr_defs = cls.__ATTR_DEF__
        obj = cls()

        dict_value_get = dict_value.get
        
        for attr_name, attr_type in attr_defs.iteritems():
            v = dict_value_get(attr_name)
            if v is None:
                setattr(obj, attr_name, v)
                continue
            
            if type_def.TYPE_INT32 <= attr_type <= type_def.TYPE_FLOAT:
                setattr(obj, attr_name, v)
                continue
                
            if attr_type == type_def.TYPE_STRING:
                # ��TYPE_STRING������ͳһ����utf8����
                setattr(obj, attr_name, v.encode("utf-8"))
                #setattr(obj, attr_name, v)
                continue

            if attr_type == type_def.TYPE_STRIP_STRING:
                setattr(obj, attr_name, v.encode("utf-8").strip())
                continue
                
            if attr_type == type_def.TYPE_BINARY:
                setattr(obj, attr_name, cls._prase_bin_value(attr_name, v))
                continue
            
            if isinstance(attr_type, dict):
                setattr(obj, attr_name, v)
                continue

            if isinstance(attr_type, list):
                #  �յ�list����ʾ��������ݲ��ù���
                if len(attr_type) == 0:
                    setattr(obj, attr_name, v)
                    continue

                item_type = attr_type[0]

                # ��TYPE_STRING������ͳһ����utf8����
                if item_type == type_def.TYPE_STRING:
                    item_value = [str_item.encode("utf-8") if str_item is not None else None for str_item in v]
                    setattr(obj, attr_name, item_value)
                    continue

                if item_type == type_def.TYPE_STRIP_STRING:
                    item_value = [str_item.encode("utf-8").strip() if str_item is not None else None for str_item in v]
                    setattr(obj, attr_name, item_value)
                    continue

                # list����������ݣ���serializable_obj����������
                if inspect.isclass(item_type) and issubclass(item_type, SerializableObj):                     
                    tmp = [item_type.from_dict(item) for item in v]
                    setattr(obj, attr_name, tmp)
                    continue

                # ��������������κδ���
                setattr(obj, attr_name, v)
                continue
                

            # ���ֻʣ��serializable_obj���������������� 
            setattr(obj, attr_name, attr_type.from_dict(v))

        return obj

    @classmethod
    def _prase_bin_value(cls, attr_name, value):
        """
        Method:    _prase_bin_value
        Description: ������������ʽ�����Ե�ֵ������������ر�������
        Parameter: 
            attr_name: ��������
            value: ����ֵ
        Return: 
        Others: ֻ��bson����֧�ֶ�������������json��֧��
        """

        pass

    @classmethod
    def _gen_bin_value(cls, attr_name, value):
        """
        Method:    _gen_bin_value
        Description: �����������ԣ�ת��Ϊ�������л��Ķ�������������ر�������
        Parameter: 
            attr_name: ��������
            value: ����ֵ
        Return: 
        Others: 
        """

        pass
        
    def serialize(self):
        """
        Method:    serialize
        Description: �����������л�Ϊ��������
        Parameter: ��
        Return: ��������
        Others: 
        """

        pass

    @classmethod
    def deserialize(cls, bin_value): 
        """
        Method:    deserialize
        Description: �Ӷ�������������Ϊ����ʵ��
        Parameter: 
            bin_value: ��������
        Return: ����ʵ��
        Others: 
        """

        pass

    
    
class JsonSerializableObj(SerializableObj):
    """
    Class: JsonSerializableObj
    Description: Json��ʽ��������л��������л���
    Base:    SerializableObj 
    Others: 
    """

    @classmethod
    def _prase_bin_value(cls, attr_name, value):
        """
        Method:    _prase_bin_value
        Description: ������������ʽ�����Ե�ֵ
        Parameter: 
            attr_name: ��������
            value: ����ǰ������ֵ
        Return: ���Ե�ֵ
        Others: ����Json���ԣ������κδ���
        """

        return value

    @classmethod
    def _gen_bin_value(cls, attr_name, value):
        """
        Method:    _gen_bin_value
        Description: �����������ԣ�ת��Ϊ�������л��Ķ���
        Parameter: 
            attr_name: ��������
            value: ���Ե�ֵ
        Return: ���Ե�ֵ
        Others: ����Json���ԣ������κδ���
        """

        return value

    def serialize(self):
        """
        Method:    serialize
        Description: �����������л�Ϊ��������
        Parameter: ��
        Return: ��������
        Others: 
        """

        dict_value = self.to_dict()
        return json.dumps(dict_value, separators = (',', ':'))
    
    def serialize_ordered(self):
        ordered_dict_value = self.to_ordered_dict()
        return json.dumps(ordered_dict_value, separators = (',', ':'))

    @classmethod
    def deserialize(cls, bin_value): 
        """
        Method:    deserialize
        Description: �Ӷ�������������Ϊ����ʵ��
        Parameter: 
            bin_value: ��������
        Return: ����ʵ��
        Others: 
        """

        if bin_value is None:
            return None
            
        dict_value = json.loads(bin_value)   
        return cls.from_dict(dict_value)

        
class BsonSerializableObj(SerializableObj):
    """
    Class: BsonSerializableObj
    Description: Bson��ʽ��������л��������л���
    Base: 
    Others: 
    """

    @classmethod
    def _prase_bin_value(cls, attr_name, value):
        """
        Method:    _prase_bin_value
        Description: ������������ʽ�����Ե�ֵ
        Parameter: 
            attr_name: ��������
            value: ����ǰ������ֵ
        Return: ���Ե�ֵ
        Others: ֱ��ͨ��str��bson.Binary����ת��Ϊ�ַ���
        """

        return str(value)

    @classmethod
    def _gen_bin_value(cls, attr_name, value):
        """
        Method:    _gen_bin_value
        Description: �����������ԣ�ת��Ϊ�������л��Ķ���
        Parameter: 
            attr_name: ��������
            value: ���Ե�ֵ
        Return: ���Ե�ֵ
        Others: ʹ��bson.Binary��װ���ݣ�ʹ��Bson����ʶ�����Ƕ���������
        """

        return bson.Binary(value) 

    def serialize(self):
        """
        Method:    serialize
        Description: �����������л�Ϊ��������
        Parameter: ��
        Return: ��������
        Others: 
        """

        dict_value = self.to_dict()
        return bson.BSON.encode(dict_value)

    @classmethod
    def deserialize(cls, bin_value): 
        """
        Method:    deserialize
        Description: �Ӷ�������������Ϊ����ʵ��
        Parameter: 
            bin_value: ��������
        Return: ����ʵ��
        Others: 
        """

        if bin_value is None:
            return None
            
        dict_value = bson.BSON(bin_value).decode()   
        return cls.from_dict(dict_value)









