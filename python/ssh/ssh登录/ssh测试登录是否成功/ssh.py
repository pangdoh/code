import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy) #加上这句话不用担心选yes的问题，会自动选上（用ssh连接远程主机时，第一次连接时会提示是否继续进行远程连接，选择yes）

hostname = "xx.xxx.xx.xxx"
user = "root"
pwd = "xxxxxxxxx"
try:
    client.connect(hostname,username=user.strip(),password=pwd.strip())
    print("连接成功")
except Exception as e:
    print("错误")
    print(e)