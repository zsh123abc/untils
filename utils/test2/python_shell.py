import paramiko
import subprocess

# # Replace the placeholders with the appropriate values
# local_file_path = r"D:\zsh\biaozhu\biaozhu_python\utils\视频抽帧\cap.py"
# remote_server = "192.168.100.131"
# remote_user = "yd"
# remote_path = "/a4/utils"

# # Use the Windows command prompt to transfer the file via SCP and input password
# subprocess.run(f"scp  {local_file_path} {remote_user}@{remote_server}:{remote_path}", shell=True)


# create an SSH client object
ssh = paramiko.SSHClient()

# automatically add the server's host key
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# connect to the server
ssh.connect('192.168.100.131', username='yd', password='yuedong888')
stdin, stdout, stderr = ssh.exec_command('python /a4/cap2.py &')

# execute the command
# stdin, stdout, stderr = ssh.exec_command('cd /a4; python shell_test.py')

# print the output
print(stdout.read().decode())

# close the connection

ssh.close()


