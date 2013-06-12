#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class Article(MocBase):
    __MOC_NAME__ = "Article"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'article_id', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'wx_news_id', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'title', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'subject_id', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'description', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 512),
                MocAttrDef(name = 'pic_url', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 256),
                MocAttrDef(name = 'content_url', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 256),
                MocAttrDef(name = 'content', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 524288),
                MocAttrDef(name = 'push_timer', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'push_times', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 16),
                MocAttrDef(name = 'counter', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                ComplexAttrDef(name = 'group_ids', attr_type = 'GroupList', is_list = True),
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [article_id], [wx_news_id], [title], [subject_id], [description], [pic_url], [content_url], [content], [push_timer], [push_times], [counter] from tbl_Article' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "article_id", "wx_news_id", "title", "subject_id", "description", "pic_url", "content_url", "content", "push_timer", "push_times", "counter" from tbl_Article' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_Article ([moid], [article_id], [wx_news_id], [title], [subject_id], [description], [pic_url], [content_url], [content], [push_timer], [push_times], [counter]) values(?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_Article ("moid", "article_id", "wx_news_id", "title", "subject_id", "description", "pic_url", "content_url", "content", "push_timer", "push_times", "counter") values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_Article set [wx_news_id]=?1, [title]=?2, [subject_id]=?3, [description]=?4, [pic_url]=?5, [content_url]=?6, [content]=?7, [push_timer]=?8, [push_times]=?9, [counter]=?10 where [moid]=?11' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_Article set "wx_news_id"=:1, "title"=:2, "subject_id"=:3, "description"=:4, "pic_url"=:5, "content_url"=:6, "content"=:7, "push_timer"=:8, "push_times"=:9, "counter"=:10 where "moid"=:11' 
    
    article_id                     = 0
    wx_news_id                     = ''
    title                          = ''
    subject_id                     = 0
    description                    = ''
    pic_url                        = ''
    content_url                    = ''
    content                        = ''
    push_timer                     = ''
    push_times                     = ''
    counter                        = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "Article_%d" % (kw["article_id"])
    
    def get_moid(self):
        return "Article_%d" % (self.article_id)
    
    @classmethod
    def get_attr_names(cls): 
        return ('article_id',), ('wx_news_id', 'title', 'subject_id', 'description', 'pic_url', 'content_url', 'content', 'push_timer', 'push_times', 'counter')
    
    def from_db_record(self, record):
        self.article_id                     = record[1]
        self.wx_news_id                     = record[2]
        self.title                          = record[3]
        self.subject_id                     = record[4]
        self.description                    = record[5]
        self.pic_url                        = record[6]
        self.content_url                    = record[7]
        self.content                        = record[8]
        self.push_timer                     = record[9]
        self.push_times                     = record[10]
        self.counter                        = record[11]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.article_id
                , self.wx_news_id
                , self.title
                , self.subject_id
                , self.description
                , self.pic_url
                , self.content_url
                , self.content
                , self.push_timer
                , self.push_times
                , self.counter
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.wx_news_id
                , self.title
                , self.subject_id
                , self.description
                , self.pic_url
                , self.content_url
                , self.content
                , self.push_timer
                , self.push_times
                , self.counter
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class ArticleRule(MocRule):
    pass
