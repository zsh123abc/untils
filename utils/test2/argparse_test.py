import argparse

import paramiko

# ssh = paramiko.SSHClient()

# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# ssh.connect('192.168.100.131', username='yd', password='yuedong888')
# # stdin, stdout, stderr = ssh.exec_command('python /a4/cap2.py &')

parser = argparse.ArgumentParser(description="可写可不写，只是在命令行参数出现错误的时候，随着错误信息打印出来。")
parser.add_argument('-lp', '--log_path')


# # 3.进行参数解析
args = parser.parse_args() 
# # print('-------gf-------', )
log_path = args.log_path
# stdin, stdout, stderr = ssh.exec_command()

cmd="cat {} |grep -o  -P {} -A 1 | tail -n 1".format(log_path,'eta.{0,10}')
print(cmd)