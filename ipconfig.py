import os
import re
ipconfig = os.popen('ipconfig')
str = ipconfig.read()
ip_ = re.findall('IPv4 地址 . . . . . . . . . . . . : 10.(.*)\n', str)
ip = '10.'+ip_[0]
print(ip)
