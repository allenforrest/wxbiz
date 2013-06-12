#coding=gbk

DEFAULT_EAU_PORT = 7001

# IMC上获取与EAU通信的endpoint
def get_eau_endpoint(eau_ip):
    global DEFAULT_EAU_PORT
    
    return "tcp://%s:%s" % (eau_ip, DEFAULT_EAU_PORT)
    

