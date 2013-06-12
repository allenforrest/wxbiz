#coding=utf-8
import copy
import tracelog

import ale_ec_params
import command_code

class ADD_ECSpec:  
    def __init__(self, args):
        self.__agrs = args
        
    def get_cmd_code(self):
        return  command_code.ALE_ADD_ECTASK_OUTER_COMMAND

    def get_timeout(self):
        return 6
        
    def gen_request(self):
        ecspec = ale_ec_params.ECSpec()
        ecspec.ecname = 'first'
        ecspec.includeSpecInReports = False         
        ecspec.logicalReaders = ['123456']
        
        ecBoundarySpec = ale_ec_params.ECBoundarySpec()
        ecBoundarySpec.repeatPeriod = 10000
        ecBoundarySpec.duration = 5000
        ecBoundarySpec.stableSetInterval = 0
        ecBoundarySpec.whenDataAvailable = False        
        ecspec.ecBoundarySpec = ecBoundarySpec
        
        ecReportSpec = ale_ec_params.ECReportSpec()
        ecReportSpec.reportName = 'testreport'
        ecReportSpec.reportSet = 0
        
        ecFieldSpec = ale_ec_params.ECFieldSpec()
        ecFieldSpec.fieldname = 'test'
        ecFieldSpec.datatype = 'test'
        ecFieldSpec.format = 'test'
        ecFilterListMember = ale_ec_params.ECFilterListMember()
        ecFilterListMember.includeExclude = False
        ecFilterListMember.ecFieldSpec = [ecFieldSpec]
        ecFilterListMember.patList = ['']
        ecFilterSpec = ale_ec_params.ECFilterSpec()
        ecFilterSpec.filterList = [ecFilterListMember]
        ecReportSpec.ecFilterSpec = ecFilterSpec
        
        ecGroupSpec = ale_ec_params.ECGroupSpec()
        ecGroupSpec.ecFieldSpec = [copy.copy(ecFieldSpec)]
        ecGroupSpec.patternList = ['']
        ecReportSpec.ecGroupSpec = ecGroupSpec
        
        ecReportOutputSpec = ale_ec_params.ECReportOutputSpec()
        ecReportOutputSpec.includeEPC = True
        ecReportOutputSpec.includeTag = True
        ecReportOutputSpec.includeRawHex = True
        ecReportOutputSpec.includeRawDecimal = True
        ecReportOutputSpec.includeCount = True
        
        ecReportOutputFieldSpec = ale_ec_params.ECReportOutputFieldSpec()
        ecReportOutputFieldSpec.ecFieldSpec = [copy.copy(ecFieldSpec)]
        ecReportOutputFieldSpec.name = ''
        ecReportOutputFieldSpec.includeFieldSpecInReport = True        
        ecReportOutputSpec.ecReportOutputFieldSpec = [ecReportOutputFieldSpec]
        ecReportSpec.ecReportOutputSpec = ecReportOutputSpec
        
        ecspec.ecReportSpecList = [ecReportSpec]
        
        ecspec.primaryKeyFields = ['']
        
        return  ecspec.serialize()
            
    def handle_ack(self, ack):
        result = ale_ec_params.CommandResult.deserialize(ack)
        tracelog.info('ADD_ECSpec: %s' % result.description)
        



