#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class Subject(MocBase):
    __MOC_NAME__ = "Subject"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'subject_id', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'name', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'description', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 256),
                MocAttrDef(name = 'counter', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [subject_id], [name], [description], [counter] from tbl_Subject' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "subject_id", "name", "description", "counter" from tbl_Subject' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_Subject ([moid], [subject_id], [name], [description], [counter]) values(?1, ?2, ?3, ?4, ?5)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_Subject ("moid", "subject_id", "name", "description", "counter") values(:1, :2, :3, :4, :5)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_Subject set [name]=?1, [description]=?2, [counter]=?3 where [moid]=?4' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_Subject set "name"=:1, "description"=:2, "counter"=:3 where "moid"=:4' 
    
    subject_id                     = 0
    name                           = ''
    description                    = ''
    counter                        = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "Subject_%d" % (kw["subject_id"])
    
    def get_moid(self):
        return "Subject_%d" % (self.subject_id)
    
    @classmethod
    def get_attr_names(cls): 
        return ('subject_id',), ('name', 'description', 'counter')
    
    def from_db_record(self, record):
        self.subject_id                     = record[1]
        self.name                           = record[2]
        self.description                    = record[3]
        self.counter                        = record[4]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.subject_id
                , self.name
                , self.description
                , self.counter
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.name
                , self.description
                , self.counter
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class SubjectRule(MocRule):
    pass
