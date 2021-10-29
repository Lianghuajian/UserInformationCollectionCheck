#coding=utf-8
#from packaging import version
#脚本用于查找有可能获取用户隐私的sdk和代码，放在iOS项目根目录，pod update后运行该脚本
import os
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import cmp_to_key
import smtplib
import json
import time
import re
import yaml
import os.path
from ruamel import yaml

def run_cmd(cmd):
  print("cmd:")
  print(cmd)
  myProcess = subprocess.Popen('bash', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
  
  output,error = myProcess.communicate(cmd.encode('utf-8'))
  output = output.decode('utf-8')
  error = error.decode('utf-8')
  returncode = myProcess.returncode
  print("returncode:")
  print(str(returncode))
  print("error:")
  print(error)
  print("output:")
  print(output)
  return output

userinfo_dict = {"IDFA":["advertisingIdentifier"],"IDFV":["identifierForVendor"],
                "运营商信息":["CTTelephonyNetworkInfo"],
                "IP地址":["getifaddrs","ipaddress"],
                "mac地址":["sockaddr_dl","macaddress"],
                "定位":["CLLocation","CLLocationManager","CoreLocation"],
                "设备标识信息":["UIDevice"],
                "网络状态":["SCNetworkReachabilitySetCallback"],
                "粘贴板":["UIPasteboard"],
                "wifiSSID和wifiBSSID":["CNCopyCurrentNetworkInfo"]
}

results_dict = {}

for key,values in userinfo_dict.items():
    for value in values:
    # -i：忽略大小写
        results = run_cmd("grep -i -r {0} .".format(value))
        lines = results.split("\n")
        #替换xxx为需要忽略的内容
        lines = list(filter(lambda line: "userinfo_collect_result" not in line, lines))
        for line in lines:
            if key in results_dict.keys():
                if line not in results_dict[key]:
                   results_dict[key].append(line)
            else:
                results_dict[key] = [line]

with open("userinfo_collect_result.yaml","w",encoding="utf-8") as f:
    yaml.dump(results_dict,f,Dumper=yaml.RoundTripDumper,allow_unicode=True)

print("userinfo_collect_result: ",results_dict)
