#coding=gbk

import serializable_obj
import type_def


class NotifyRunningPidsMsg(serializable_obj.BsonSerializableObj): 
    __ATTR_DEF__ = {
                      "running_pids": [type_def.TYPE_UINT32]
                    }

