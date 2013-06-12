#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-12
Description: 序列化和反序列化类，提供了两种编码方式: Json和Bson
             可以通过继承JsonSerializableObj或BsonSerializableObj来自定义数据结构
Others:      
Key Class&Method List: 
             1. SerializableObj: JsonSerializableObj和BsonSerializableObj的基类
             2. JsonSerializableObj: Json方式编码的序列化、反序列化类
             3. BsonSerializableObj: Bson方式编码的序列化、反序列化类


注: 
 1) 目前没有采用cPickle，主要因为其数据格式不紧凑，数据格式不通用
 2) 定义为type_def.TYPE_STRING的属性，或 [type_def.TYPE_STRING]的属性，都会在反序列化时，将unicode自动转换为普通的string
    其他情况下的字符串，反序列化后，仍然是unicode。例如字典类型的属性，其key就是unicode



举例:

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
    Description: JsonSerializableObj和BsonSerializableObj的基类
    Base: 
    Others: 
    """

    
    __ATTR_DEF__ = None
    
    def __init__(self):
        pass


    def init_all_attr(self):
        """
        Method:    init_all_attr
        Description: 根据__ATTR_DEF__中定义的属性名称，自动构造所有的属性，属性值为None
        Parameter: 无
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
        Description: 根据对象的所有属性，生成bson和json能够使用的字典
        Parameter: 无
        Return: 包含了所有属性值的字典
        Others: 属性也可以是序列化的类类型的
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
                #  空的list，表示里面的内容不用关心
                if len(attr_type) == 0:
                    #dict_value[attr_name] = v
                    dict_list.insert(index, (attr_name, v))
                    continue

                item_type = attr_type[0]
                
                # list中如果有内容，且serializable_obj派生的子类
                if inspect.isclass(item_type) and issubclass(item_type, SerializableObj):                     
                    tmp = [item.to_dict() if item is not None else None for item in v]
                    #dict_value[attr_name] = tmp
                    dict_list.insert(index, (attr_name, tmp))
                    continue

                # 其他情况，不做任何处理
                #dict_value[attr_name] = v
                dict_list.insert(index, (attr_name, v))
                continue

            # 最后，只剩下serializable_obj派生的子类的情况了 
            #dict_value[attr_name] = v.to_dict()
            dict_list.insert(index, (attr_name, v.to_ordered_dict()))

        dict_value = collections.OrderedDict(dict_list)
        return dict_value
         

    def to_dict(self):
        """
        Method:    to_dict
        Description: 根据对象的所有属性，生成bson和json能够使用的字典
        Parameter: 无
        Return: 包含了所有属性值的字典
        Others: 属性也可以是序列化的类类型的
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
                #  空的list，表示里面的内容不用关心
                if len(attr_type) == 0:
                    dict_value[attr_name] = v
                    continue

                item_type = attr_type[0]
                
                # list中如果有内容，且serializable_obj派生的子类
                if inspect.isclass(item_type) and issubclass(item_type, SerializableObj):                     
                    tmp = [item.to_dict() if item is not None else None for item in v]
                    dict_value[attr_name] = tmp
                    continue

                # 其他情况，不做任何处理
                dict_value[attr_name] = v
                continue

            # 最后，只剩下serializable_obj派生的子类的情况了 
            dict_value[attr_name] = v.to_dict()

        return dict_value

    @classmethod
    def from_dict(cls, dict_value):
        """
        Method:    from_dict
        Description: 根据字典，生成当对象实例，其属性的值就是字典中同名key对应的值
        Parameter: 
            dict_value: 字典，包含了对象实例的属性值
        Return: 对象实例
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
                # 对TYPE_STRING的属性统一采用utf8编码
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
                #  空的list，表示里面的内容不用关心
                if len(attr_type) == 0:
                    setattr(obj, attr_name, v)
                    continue

                item_type = attr_type[0]

                # 对TYPE_STRING的属性统一采用utf8编码
                if item_type == type_def.TYPE_STRING:
                    item_value = [str_item.encode("utf-8") if str_item is not None else None for str_item in v]
                    setattr(obj, attr_name, item_value)
                    continue

                if item_type == type_def.TYPE_STRIP_STRING:
                    item_value = [str_item.encode("utf-8").strip() if str_item is not None else None for str_item in v]
                    setattr(obj, attr_name, item_value)
                    continue

                # list中如果有内容，且serializable_obj派生的子类
                if inspect.isclass(item_type) and issubclass(item_type, SerializableObj):                     
                    tmp = [item_type.from_dict(item) for item in v]
                    setattr(obj, attr_name, tmp)
                    continue

                # 其他情况，不做任何处理
                setattr(obj, attr_name, v)
                continue
                

            # 最后，只剩下serializable_obj派生的子类的情况了 
            setattr(obj, attr_name, attr_type.from_dict(v))

        return obj

    @classmethod
    def _prase_bin_value(cls, attr_name, value):
        """
        Method:    _prase_bin_value
        Description: 解析二进制形式的属性的值，子类可以重载本方法。
        Parameter: 
            attr_name: 属性名称
            value: 属性值
        Return: 
        Others: 只有bson可以支持二进制数据流，json不支持
        """

        pass

    @classmethod
    def _gen_bin_value(cls, attr_name, value):
        """
        Method:    _gen_bin_value
        Description: 将二进制属性，转换为可以序列化的对象，子类可以重载本方法。
        Parameter: 
            attr_name: 属性名称
            value: 属性值
        Return: 
        Others: 
        """

        pass
        
    def serialize(self):
        """
        Method:    serialize
        Description: 将本对象序列化为二进制流
        Parameter: 无
        Return: 二进制流
        Others: 
        """

        pass

    @classmethod
    def deserialize(cls, bin_value): 
        """
        Method:    deserialize
        Description: 从二进制流反序列为对象实例
        Parameter: 
            bin_value: 二进制流
        Return: 对象实例
        Others: 
        """

        pass

    
    
class JsonSerializableObj(SerializableObj):
    """
    Class: JsonSerializableObj
    Description: Json方式编码的序列化、反序列化类
    Base:    SerializableObj 
    Others: 
    """

    @classmethod
    def _prase_bin_value(cls, attr_name, value):
        """
        Method:    _prase_bin_value
        Description: 解析二进制形式的属性的值
        Parameter: 
            attr_name: 属性名称
            value: 解析前的属性值
        Return: 属性的值
        Others: 对于Json而言，不做任何处理
        """

        return value

    @classmethod
    def _gen_bin_value(cls, attr_name, value):
        """
        Method:    _gen_bin_value
        Description: 将二进制属性，转换为可以序列化的对象
        Parameter: 
            attr_name: 属性名称
            value: 属性的值
        Return: 属性的值
        Others: 对于Json而言，不做任何处理
        """

        return value

    def serialize(self):
        """
        Method:    serialize
        Description: 将本对象序列化为二进制流
        Parameter: 无
        Return: 二进制流
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
        Description: 从二进制流反序列为对象实例
        Parameter: 
            bin_value: 二进制流
        Return: 对象实例
        Others: 
        """

        if bin_value is None:
            return None
            
        dict_value = json.loads(bin_value)   
        return cls.from_dict(dict_value)

        
class BsonSerializableObj(SerializableObj):
    """
    Class: BsonSerializableObj
    Description: Bson方式编码的序列化、反序列化类
    Base: 
    Others: 
    """

    @classmethod
    def _prase_bin_value(cls, attr_name, value):
        """
        Method:    _prase_bin_value
        Description: 解析二进制形式的属性的值
        Parameter: 
            attr_name: 属性名称
            value: 解析前的属性值
        Return: 属性的值
        Others: 直接通过str将bson.Binary对象转换为字符串
        """

        return str(value)

    @classmethod
    def _gen_bin_value(cls, attr_name, value):
        """
        Method:    _gen_bin_value
        Description: 将二进制属性，转换为可以序列化的对象
        Parameter: 
            attr_name: 属性名称
            value: 属性的值
        Return: 属性的值
        Others: 使用bson.Binary包装数据，使得Bson可以识别这是二进制数据
        """

        return bson.Binary(value) 

    def serialize(self):
        """
        Method:    serialize
        Description: 将本对象序列化为二进制流
        Parameter: 无
        Return: 二进制流
        Others: 
        """

        dict_value = self.to_dict()
        return bson.BSON.encode(dict_value)

    @classmethod
    def deserialize(cls, bin_value): 
        """
        Method:    deserialize
        Description: 从二进制流反序列为对象实例
        Parameter: 
            bin_value: 二进制流
        Return: 对象实例
        Others: 
        """

        if bin_value is None:
            return None
            
        dict_value = bson.BSON(bin_value).decode()   
        return cls.from_dict(dict_value)









