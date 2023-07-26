import paramiko

# create an SSH client object
ssh = paramiko.SSHClient()

# automatically add the server's host key
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# connect to the server
ssh.connect('hostname', username='username', password='password')

# execute the command
stdin, stdout, stderr = ssh.exec_command('command')

# print the output
print(stdout.read().decode())

# close the connection
ssh.close()


