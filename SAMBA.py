# -*- coding:UTF-8 -*-
# 作者：张子涵

# 删除用户 net use * /del
import os,re

class Configure_Samba():
    def __init__(self):
        pass
    def backup(self):
        # 检测是否存在/backup目录，如果不存在则创建，存在则不创建
        if not os.path.exists("/backup"):
            # 检测是否存在/etc/samba/smb.conf配置文件，如果不存在则提示系统未安装vsftpd服务
            if not os.path.exists("/etc/samba/smb.conf"):
                info = "系统未检测到smb服务，请安装！"
                return info

            else:
                # 创建/backup目录，并将samba主配置文件备份到/backup目录
                # 以后运行服务出现问题，可以通过备份进行还原
                os.mkdir("/backup")
                os.system("cp -rf /etc/samba/smb.conf /backup")

        else:
            if not os.path.exists("/etc/samba/smb.conf"):
                info = "系统未检测到smb服务，请安装！"
                return info

            else:
                # 当/backup目录已存在，程序则不会创建/backup目录
                # 程序直接开始备份
                os.system("cp -rf /etc/samba/smb.conf /backup")

    def configure_anonymous_access(self):
        smb_file = r"/etc/samba/smb.conf"
        local_smb_file = r"./smb.conf"

        with open(local_smb_file,"r",encoding="utf-8") as f:
            content = f.read()
        bad_user = re.findall("map to guest = bad user",content)
        bad_user = bad_user[0]

        share = re.findall('''\[share\]
	path = /opt/share
	writeable = yes
	guest ok = yes''',content)
        share = share[0]

        path = re.findall("path = (.*)",share)
        path = path[0]


        writable = re.findall("writeable = .*",share)
        writable = writable[0]

        guest_ok = re.findall("guest ok = .*",share)
        guest_ok = guest_ok[0]

        anonymous_enable = input("是否允许匿名访问(y/n/空格默认拒绝):")
        if anonymous_enable.lower() == "y":
            path_value = input("请输入共享文件夹的路径:")
            if not os.path.exists(path_value):
                print("系统为检测到%s目录，正在为您创建！！！"%path_value)
                os.system("mkdir -p %s"%path_value)
                os.system("chmod -R 777 %s"%path_value)
                print("创建成功！")
            else:
                os.system("chmod -R 777 %s" % path_value)
            writable_value = input("是否允许共享目录写入权限(yes/no):")
            guest_ok_value = input("所有用户是否访问共享目录(yes/no):")
            if path_value == "" and writable_value == "" and guest_ok_value == "":
                print("您不能输入空值！")
            else:
                content = content.replace(path,path_value).replace(writable,"writeable = "+writable_value.lower()).replace(guest_ok,"guest ok = "+guest_ok_value.lower())
                with open(smb_file,"w",encoding="utf-8") as f:
                    f.write(content)
        else:
            content = content.replace(bad_user,"").replace(share,"")
            with open(smb_file, "w", encoding="utf-8") as f:
                f.write(content)

    # def configure_samba_user(self):
    #     smb_file = r"/etc/samba/smb.conf"
    #     local_smb_file = r"./smb.conf"
    #     with open(local_smb_file,"r",encoding="utf-8") as f:
    #         content = f.read()
    #
    #     valid_user = "valid users = "
    #     write_list = "write list = "
    #
    #     samba_enable = input(":")
    #     if samba_enable.lower() == "y":
    #         path = input(":")
    #         valid_user = input(":")
    #         write_list = input(":")
    #         content = content.replace("writeable = yes")

if __name__ == '__main__':
    a = Configure_Samba()
    a.configure_anonymous_access()
