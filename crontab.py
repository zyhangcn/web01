import paramiko

client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(hostname='101.132.159.77',port=22,username="zyh",password='hang521.')
stin,stout,stderr=client.exec_command("ls ~")
print(dir(stout))
print(type(stout.read()))
print(stout.read().decode())

client.close()