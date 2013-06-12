#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class Subscriber(MocBase):
    __MOC_NAME__ = "Subscriber"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'subscriber_open_id', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'subscribe_seq_no', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'fake_id', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'weixin_id', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'nickname', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 128),
                MocAttrDef(name = 'gender', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 16),
                MocAttrDef(name = 'city', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 32),
                MocAttrDef(name = 'sub_time', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'group_id', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'assoc_member_id', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 32),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [subscriber_open_id], [subscribe_seq_no], [fake_id], [weixin_id], [nickname], [gender], [city], [sub_time], [group_id], [assoc_member_id] from tbl_Subscriber' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "subscriber_open_id", "subscribe_seq_no", "fake_id", "weixin_id", "nickname", "gender", "city", "sub_time", "group_id", "assoc_member_id" from tbl_Subscriber' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_Subscriber ([moid], [subscriber_open_id], [subscribe_seq_no], [fake_id], [weixin_id], [nickname], [gender], [city], [sub_time], [group_id], [assoc_member_id]) values(?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_Subscriber ("moid", "subscriber_open_id", "subscribe_seq_no", "fake_id", "weixin_id", "nickname", "gender", "city", "sub_time", "group_id", "assoc_member_id") values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_Subscriber set [subscribe_seq_no]=?1, [fake_id]=?2, [weixin_id]=?3, [nickname]=?4, [gender]=?5, [city]=?6, [sub_time]=?7, [group_id]=?8, [assoc_member_id]=?9 where [moid]=?10' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_Subscriber set "subscribe_seq_no"=:1, "fake_id"=:2, "weixin_id"=:3, "nickname"=:4, "gender"=:5, "city"=:6, "sub_time"=:7, "group_id"=:8, "assoc_member_id"=:9 where "moid"=:10' 
    
    subscriber_open_id             = ''
    subscribe_seq_no               = 0
    fake_id                        = ''
    weixin_id                      = ''
    nickname                       = ''
    gender                         = ''
    city                           = ''
    sub_time                       = ''
    group_id                       = 0
    assoc_member_id                = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "Subscriber_%s" % (repr(kw["subscriber_open_id"]))
    
    def get_moid(self):
        return "Subscriber_%s" % (repr(self.subscriber_open_id))
    
    @classmethod
    def get_attr_names(cls): 
        return ('subscriber_open_id',), ('subscribe_seq_no', 'fake_id', 'weixin_id', 'nickname', 'gender', 'city', 'sub_time', 'group_id', 'assoc_member_id')
    
    def from_db_record(self, record):
        self.subscriber_open_id             = record[1]
        self.subscribe_seq_no               = record[2]
        self.fake_id                        = record[3]
        self.weixin_id                      = record[4]
        self.nickname                       = record[5]
        self.gender                         = record[6]
        self.city                           = record[7]
        self.sub_time                       = record[8]
        self.group_id                       = record[9]
        self.assoc_member_id                = record[10]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.subscriber_open_id
                , self.subscribe_seq_no
                , self.fake_id
                , self.weixin_id
                , self.nickname
                , self.gender
                , self.city
                , self.sub_time
                , self.group_id
                , self.assoc_member_id
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.subscribe_seq_no
                , self.fake_id
                , self.weixin_id
                , self.nickname
                , self.gender
                , self.city
                , self.sub_time
                , self.group_id
                , self.assoc_member_id
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class SubscriberRule(MocRule):
    pass
