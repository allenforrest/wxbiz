#coding=gbk

DEFAULT_EAU_PORT = 7001

# IMC�ϻ�ȡ��EAUͨ�ŵ�endpoint
def get_eau_endpoint(eau_ip):
    global DEFAULT_EAU_PORT
    
    return "tcp://%s:%s" % (eau_ip, DEFAULT_EAU_PORT)
    

