#coding=utf-8

import serializable_obj
import type_def

class ECBoundarySpec(serializable_obj.JsonSerializableObj):
    __ATTR_DEF__ = {
                      "repeatPeriod":type_def.TYPE_UINT32
                    , "duration": type_def.TYPE_UINT32
                    , "stableSetInterval": type_def.TYPE_UINT32
                    , "whenDataAvailable": type_def.TYPE_BOOL
                    }                     
    
class ECFieldSpec(serializable_obj.JsonSerializableObj):
    __ATTR_DEF__ = {
                      "fieldname":type_def.TYPE_STRING
                    , "datatype": type_def.TYPE_STRING
                    , "format": type_def.TYPE_STRING                    
                    }
class ECFilterListMember(serializable_obj.JsonSerializableObj):
    __ATTR_DEF__ = {
                      "includeExclude":type_def.TYPE_BOOL
                    , "ecFieldSpec": [ECFieldSpec]
                    , "patList": []                    
                    }
    
class ECFilterSpec(serializable_obj.JsonSerializableObj):
    __ATTR_DEF__ = {
                      "filterList": [ECFilterListMember]
                    ,                    
                    }

class ECGroupSpec(serializable_obj.JsonSerializableObj):
    __ATTR_DEF__ = {
                      "ecFieldSpec": [ECFieldSpec]
                    , "patternList": []                    
                    }
class ECReportOutputFieldSpec(serializable_obj.JsonSerializableObj):
    __ATTR_DEF__ = {
                      "ecFieldSpec": [ECFieldSpec]
                    , "name": type_def.TYPE_STRING
                    , "includeFieldSpecInReport": type_def.TYPE_BOOL                   
                    }
class ECReportOutputSpec(serializable_obj.JsonSerializableObj):
    __ATTR_DEF__ = {
                      "includeEPC": type_def.TYPE_BOOL
                    , "includeTag": type_def.TYPE_BOOL
                    , "includeRawHex": type_def.TYPE_BOOL                   
                    , "includeRawDecimal": type_def.TYPE_BOOL
                    , "includeCount": type_def.TYPE_BOOL
                    , "ecReportOutputFieldSpec": [ECReportOutputFieldSpec]                    
                    }
                
class ECReportSpec(serializable_obj.JsonSerializableObj):
    
    __ATTR_DEF__ = {
                      "reportName":type_def.TYPE_STRING
                    , "reportSet": type_def.TYPE_UINT16
                    , "ecFilterSpec": ECFilterSpec
                    , "ecGroupSpec": ECGroupSpec
                    , "ecReportOutputSpec": ECReportOutputSpec
                    } 

    
class ECSpec(serializable_obj.JsonSerializableObj):   
    __ATTR_DEF__ = {                      
                      "ecname": type_def.TYPE_STRING
                    , "logicalReaders": []
                    , "ecBoundarySpec": ECBoundarySpec                    
                    , "ecReportSpecList" : [ECReportSpec]
                    , "includeSpecInReports" : type_def.TYPE_BOOL
                    , "primaryKeyFields" : []
                    }
    
class CommandResult(serializable_obj.JsonSerializableObj):
    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    }