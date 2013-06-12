#coding=gbk
import copy
import tracelog

import ale_ec_params
import message_across_app
import command_code
class sub_ECSpec:  
    def __init__(self, args):
        self.__agrs = args
        
    def get_cmd_code(self):
        return  command_code.ALE_ADD_SUBSCRIBE_ECTASK_COMMAND

    def get_timeout(self):
        return 6
        
    def gen_request(self):        
        ecspec_sub = message_across_app.EcspecSubscribe()
        ecspec_sub.ecname = 'first'
        ecspec_sub.notificationURI = 'tcp://127.0.0.1:808'        
        

        return ecspec_sub.serialize()
            
    def handle_ack(self, ack):
        result = ale_ec_params.CommandResult.deserialize(ack)
        tracelog.info('sub_ECSpec: %s' % result.description)
        



