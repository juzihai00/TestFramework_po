import paramiko

class SSH:
    """
    ssh远程连接
    """
    def __init__(self,ip,username,password,port=22):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port

    def shell_cmd(self,cmd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip,port=self.port,username=self.username,password=self.password,timeout=10)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            content = stdout.read().decode('utf-8')
            res = content.split('\n')
            ssh.close()
            return res
        except Exception as e:
            print("远程执行shell命令失败")
            return False

    def shell_upload(self,local_path,remote_path):
        """
        远程上传文件
        :return:
        """
        try:
            transport = paramiko.Transport((self.ip,self.port))
            transport.connect(username=self.username,password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(local_path,remote_path)
            transport.close()
            print("文件上传成功，上传路径：{}".format(remote_path))
        except Exception as e:
            print("文件上传失败！{}".format(e))
            return False

    def shell_download(self,remote_path,local_path):
        """
        远程下载文件
        :return:
        """
        try:
            transport = paramiko.Transport((self.ip,self.port))
            transport.connect(username=self.username,password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.get(remote_path,local_path)
            transport.close()
            print("文件下载成功，下载地址{}".format(local_path))
            return True
        except Exception as e:
            print("文件下载失败{}".format(e))
            return False
