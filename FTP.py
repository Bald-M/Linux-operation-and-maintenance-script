# -*- coding:UTF-8 -*-
# 作者：张子涵


import os
class Configure_FTP():
    def __init__(self):
        pass
    # 函数 备份
    def backup(self):
        # 检测是否存在/backup目录，如果不存在则创建，存在则不创建
        if not os.path.exists("/backup"):
            # 检测是否存在/etc/vsftpd/vsftpd.conf配置文件，如果不存在则提示系统未安装vsftpd服务
            if not os.path.exists("/etc/vsftpd/vsftpd.conf"):
                info = "系统未检测到vsftpd服务，请安装！"
                return info

            else:
                # 创建/backup目录，并将vsftpd主配置文件备份到/backup目录
                # 以后运行服务出现问题，可以通过备份进行还原
                os.mkdir("/backup")
                os.system("cp -rf /etc/vsftpd/vsftpd.conf /backup")

        else:
            if not os.path.exists("/etc/vsftpd/vsftpd.conf"):
                info = "系统未检测到vsftpd服务，请安装！"
                return info

            else:
                # 当/backup目录已存在，程序则不会创建/backup目录
                # 程序直接开始备份
                os.system("cp -rf /etc/vsftpd/vsftpd.conf /backup")


    # 函数 配置匿名用户
    def config_anonymous_users(self):
        # ftp_file表示ftp的主配置文件路径
        ftp_file = r"/etc/vsftpd/vsftpd.conf"

        # local_ftp_file表示本地ftp配置文件
        local_ftp_file = r"./vsftpd.conf"

        # 匿名用户配置项
        anon_enable = os.popen(r"sed -n '/anonymous_enable/p' %s "%local_ftp_file)
        anon_enable_info = anon_enable.read().strip()
        anon_umask = os.popen(r"sed -n '/anon_umask/p' %s"%local_ftp_file)
        anon_umask_info = anon_umask.read().strip()
        anon_root = os.popen(r"sed -n '/anon_root/p' %s"%local_ftp_file)
        anon_root_info = anon_root.read().strip()
        anon_upload_enable = os.popen(r"sed -n '/anon_upload_enable/p' %s"%local_ftp_file)
        anon_upload_enable_info = anon_upload_enable.read().strip()
        anon_mkdir_write_enable = os.popen(r"sed -n '/anon_mkdir_write_enable/p' %s"%local_ftp_file)
        anon_mkdir_write_enable_info = anon_mkdir_write_enable.read().strip()
        anon_other_write_enable = os.popen(r"sed -n '/anon_other_write_enable/p' %s"%local_ftp_file)
        anon_other_write_enable_info = anon_other_write_enable.read().strip()
        anon_max_rate = os.popen(r"sed -n '/anon_max_rate/p' %s "%local_ftp_file)
        anon_max_rate_info = anon_max_rate.read().strip()

        allow_anonymous = input("是否允许匿名用户(y/n/回车默认拒绝)：")

        if allow_anonymous.lower() == "y":
            # 允许匿名访问 不管之前的anonymous_enable是什么状态，程序都会改成YES
            os.system(r"sed -i 's/%s/anonymous_enable=YES/' %s"%(anon_enable_info,local_ftp_file))

            # 设置匿名用户上传文件的权限掩码值,如果输入回车或其他类型则权限掩码值为022，不懂就回车
            anon_umask_config = input("请输入匿名用户所上传文件的默认权限掩码值（回车默认022）：")
            if anon_umask_config == "":
                os.system(r"sed -i 's/%s/anon_umask=022/' %s " % (anon_umask_info, local_ftp_file))
            elif anon_umask_config.isdigit():
                os.system(r"sed -i 's/%s/anon_umask=%s/' %s " % (anon_umask_info, anon_umask_config, local_ftp_file))
            else:
                os.system(r"sed -i 's/%s/anon_umask=022/' %s " % (anon_umask_info, local_ftp_file))

            # 设置匿名用户的根目录，如果输入回车则默认选择/var/ftp为根目录，请输入绝对路径，输入其他字符类型重启服务就会报错，不懂就回车
            anon_root_path = input("请输入匿名用户的根目录（回车默认设置路径为/var/ftp）：")
            if anon_root_path == "":
                os.system(r"sed -i '/anon_root/s/%s/anon_root=\/var\/ftp/g' %s"%(anon_root_info.replace("/","\/"),local_ftp_file))
            else:
                os.system(r"sed -i '/anon_root/s/%s/anon_root=%s/g' %s"%(anon_root_info.replace("/","\/"),anon_root_path.replace("/","\/"),local_ftp_file))

            # 设置匿名用户上传权限，只能输入y或n，输入其他字符类型则默认拒绝上传文件，不懂就回车
            enable_anon_upload = input("是否允许匿名用户上传文件(y/n/回车默认拒绝)：")
            if enable_anon_upload.lower() == "y":
                # 允许匿名用户上传文件
                os.system("sed -i '/anon_upload_enable/s/%s/anon_upload_enable=YES/g' %s "%(anon_upload_enable_info.replace("/","\/"),local_ftp_file))
            elif enable_anon_upload.lower() == "n":
                # 禁止匿名用户上传文件
                os.system("sed -i '/anon_upload_enable/s/%s/anon_upload_enable=NO/g' %s "%(anon_upload_enable_info.replace("/","\/"),local_ftp_file))
            else:
                # 禁止匿名用户上传文件
                os.system("sed -i '/anon_upload_enable/s/%s/anon_upload_enable=NO/g' %s " % (
                anon_upload_enable_info.replace("/", "\/"), local_ftp_file))

            # 设置匿名用户创建文件权限，只能输入y或n，输入其他字符类型则默认拒绝创建文件，不懂就回车
            anon_mkdir_write = input("是否允许匿名用户创建文件(y/n/回车默认拒绝)：")
            # 允许匿名用户创建文件
            if anon_mkdir_write.lower() == "y":
                os.system("sed -i '/anon_mkdir_write_enable/s/%s/anon_mkdir_write_enable=YES/g' %s "%(anon_mkdir_write_enable_info.replace("/","\/"),local_ftp_file))
            # 拒绝匿名用户创建文件
            elif anon_mkdir_write.lower() == "n":
                os.system("sed -i '/anon_mkdir_write_enable/s/%s/anon_mkdir_write_enable=NO/g' %s "%(anon_mkdir_write_enable_info.replace("/","\/"),local_ftp_file))
            # 拒绝匿名用户创建文件
            else:
                os.system("sed -i '/anon_mkdir_write_enable/s/%s/anon_mkdir_write_enable=NO/g' %s " % (
                anon_mkdir_write_enable_info.replace("/", "\/"), local_ftp_file))

            # 配置匿名用户其他写入权限，只能输入y或n，输入其他字符默认拒绝
            anon_other_write_enable = input("是否允许匿名用户有其他写入权限，如对文件改名、覆盖及删除文件等(y/n/回车默认拒绝)：")
            # 允许匿名用户拥有其他写入权限
            if anon_other_write_enable.lower() == "y":
                os.system("sed -i '/anon_other_write_enable/s/%s/anon_other_write_enable=YES/g' %s "%(anon_other_write_enable_info.replace("/","\/"),local_ftp_file))
            # 拒绝匿名用户拥有其他写入权限
            elif anon_other_write_enable.lower() == "n":
                os.system("sed -i '/anon_other_write_enable/s/%s/anon_other_write_enable=NO/g' %s "%(anon_other_write_enable_info.replace("/","\/"),local_ftp_file))
            # 拒绝匿名用户拥有其他写入权限
            else:
                os.system("sed -i '/anon_other_write_enable/s/%s/anon_other_write_enable=NO/g' %s " % (
                anon_other_write_enable_info.replace("/", "\/"), local_ftp_file))

            # 配置最大传输速率，回车或输入其他字符默认为0
            anon_max_rate_config = input("请输入最大传输速率（0代表无限制/回车默认为0）：")
            if anon_max_rate_config == "":
                os.system(r"sed -i 's/%s/anon_max_rate=0/' %s " % (anon_max_rate_info, local_ftp_file))
            elif anon_max_rate_config.isdigit():
                os.system(
                    r"sed -i 's/%s/anon_max_rate=%s/' %s " % (anon_max_rate_info, anon_max_rate_config, local_ftp_file))
            else:
                os.system(r"sed -i 's/%s/anon_max_rate=0/' %s " % (anon_max_rate_info, local_ftp_file))

        # 拒绝匿名用户访问
        elif allow_anonymous.lower() == "n":
            os.system(r"sed -i 's/%s/anonymous_enable=NO/' %s" % (anon_enable_info,local_ftp_file))
            #anon_umask
            os.system(r"sed -i 's/%s/#anon_umask=022/' %s " % (anon_umask_info, local_ftp_file))
            #anon_root
            os.system(r"sed -i 's/%s/#%s/' %s"%(anon_root_info.replace("/","\/"),anon_root_info.replace("/","\/"),local_ftp_file))
            #anon_upload
            os.system(r"sed -i 's/%s/#%s/' %s"%(anon_upload_enable_info.replace("/","\/"),anon_upload_enable_info.replace("/","\/"),local_ftp_file))
            #anon_mkdir_write
            os.system(r"sed -i 's/%s/#%s/' %s" % (
            anon_mkdir_write_enable_info.replace("/", "\/"), anon_mkdir_write_enable_info.replace("/", "\/"), local_ftp_file))
            #anon_other_write
            os.system(r"sed -i 's/%s/#%s/' %s" % (
                anon_other_write_enable_info.replace("/", "\/"), anon_other_write_enable_info.replace("/", "\/"),
                local_ftp_file))
            #anon_max_rate
            os.system(r"sed -i 's/%s/#%s/' %s " % (anon_max_rate_info.replace("/","\/"),anon_max_rate_info.replace("/","\/"),local_ftp_file))

        else:
            os.system(r"sed -i 's/%s/anonymous_enable=NO/' %s" % (anon_enable_info, local_ftp_file))
            # anon_umask
            os.system(r"sed -i 's/%s/#anon_umask=022/' %s " % (anon_umask_info, local_ftp_file))
            # anon_root
            os.system(r"sed -i 's/%s/#%s/' %s" % (
            anon_root_info.replace("/", "\/"), anon_root_info.replace("/", "\/"), local_ftp_file))
            # anon_upload
            os.system(r"sed -i 's/%s/#%s/' %s" % (
            anon_upload_enable_info.replace("/", "\/"), anon_upload_enable_info.replace("/", "\/"), local_ftp_file))
            # anon_mkdir_write
            os.system(r"sed -i 's/%s/#%s/' %s" % (
                anon_mkdir_write_enable_info.replace("/", "\/"), anon_mkdir_write_enable_info.replace("/", "\/"),
                local_ftp_file))
            # anon_other_write
            os.system(r"sed -i 's/%s/#%s/' %s" % (
                anon_other_write_enable_info.replace("/", "\/"), anon_other_write_enable_info.replace("/", "\/"),
                local_ftp_file))
            # anon_max_rate
            os.system(r"sed -i 's/%s/#%s/' %s " % (
            anon_max_rate_info.replace("/", "\/"), anon_max_rate_info.replace("/", "\/"), local_ftp_file))


        local_ftp_content = open(local_ftp_file,"r")
        local_ftp_content = local_ftp_content.read()
        with open(ftp_file,"w",encoding="utf-8") as f:
            f.write(local_ftp_content)

    # 配置全局权限，通常配合本地用户
    def global_config(self):
        # ftp主要配置文件
        ftp_file = r"/etc/vsftpd/vsftpd.conf"

        # 全局配置项
        write_enable = os.popen(r"sed -n '/^write_enable/p' %s"%ftp_file)
        write_enable_info = write_enable.read().strip()
        download_enable = os.popen(r"sed -n '/download_enable/p' %s "%ftp_file)
        download_enable_info = download_enable.read().strip()
        userlist_enable = os.popen(r"sed -n '/userlist_enable/p' %s "%ftp_file)
        userlist_enable_info = userlist_enable.read().strip()
        userlist_deny = os.popen(r"sed -n '/userlist_deny/p' %s"%ftp_file)
        userlist_deny_info = userlist_deny.read().strip()
        max_clients = os.popen(r"sed -n '/max_clients/p' %s " % ftp_file)
        max_clients_info = max_clients.read().strip()
        max_per_ip = os.popen(r"sed -n '/max_per_ip/p' %s "%ftp_file)
        max_per_ip_info = max_per_ip.read().strip()
        listen = os.popen(r"sed -n '/^listen=/p' %s "%ftp_file)
        listen_info = listen.read().strip()
        listen_address = os.popen(r"sed -n '/listen_address/p' %s "%ftp_file)
        listen_address_info = listen_address.read().strip()
        listen_port = os.popen(r"sed -n '/listen_port/p' %s "%ftp_file)
        listen_port_info = listen_port.read().strip()

        # 配置写入权限，只能输入y或n，输入其他则拒绝
        enable_write = input("是否启用任何形式的写入权限（如上传、删除文件等）都需要开启此选项(y/n/回车默认拒绝)：")
        # 允许写入
        if enable_write.lower() == "y":
            os.system(r"sed -i 's/%s/write_enable=YES/' %s" % (write_enable_info, ftp_file))
        # 拒绝写入
        elif enable_write.lower() == "n":
            os.system(r"sed -i 's/%s/write_enable=NO/' %s" % (write_enable_info, ftp_file))
        # 拒绝写入
        else:
            os.system(r"sed -i 's/%s/write_enable=NO/' %s" % (write_enable_info, ftp_file))

        # 配置下载权限，只能输入y或n，输入其他则拒绝
        enable_download = input("是否允许下载文件（建立仅限于浏览、上传的FTP服务器时可将其设为No）(y/n/回车默认拒绝)：")
        # 允许下载
        if enable_download.lower() == "y":
            os.system(r"sed -i 's/%s/download_enable=YES/' %s"%(download_enable_info,ftp_file))
        # 拒绝下载
        elif enable_download.lower() == "n":
            os.system(r"sed -i 's/%s/download_enable=NO/' %s"%(download_enable_info,ftp_file))
        # 拒绝下载
        else:
            os.system(r"sed -i 's/%s/download_enable=NO/' %s" % (download_enable_info, ftp_file))

        # 只能输入y或n，输入其他默认不启用
        enable_userlist = input("是否启用user_list用户列表文件(y/n/回车默认不启用)：")
        # 启用user_list
        if enable_userlist.lower() == "y":
            os.system(r"sed -i 's/%s/userlist_enable=YES/' %s"%(userlist_enable_info,ftp_file))
        # 不启用user_list
        elif enable_userlist.lower() == "n":
            os.system(r"sed -i 's/%s/userlist_enable=NO/' %s"%(userlist_enable_info,ftp_file))
        # 不启用user_list
        else:
            os.system(r"sed -i 's/%s/userlist_enable=NO/' %s" % (userlist_enable_info, ftp_file))

        # 只能输入y或n，输入其他默认禁止
        deny_userlist = input("是否禁止user_list列表文件中的用户账号(y/n/回车默认禁止)：")
        # 设置user_list为黑名单
        if deny_userlist.lower() == "y":
            os.system(r"sed -i 's/%s/userlist_deny=YES/' %s"%(userlist_deny_info,ftp_file))
        # 设置user_list为白名单
        elif deny_userlist.lower() == "n":
            os.system(r"sed -i 's/%s/userlist_deny=NO/' %s"%(userlist_deny_info,ftp_file))
        # 设置user_list为白名单
        else:
            os.system(r"sed -i 's/%s/userlist_deny=NO/' %s" % (userlist_deny_info, ftp_file))

        # 配置最大用户连接数
        max_connection = input("最多允许多少用户同时登录（回车默认不做限制）：")
        if max_connection.isdigit():
            os.system(r"sed -i 's/%s/max_clients=%s/' %s" % (max_clients_info, max_connection, ftp_file))
        else:
            os.system(r"sed -i 's/%s/max_clients=0/' %s"%(max_clients_info,ftp_file))

        # 配置最多文件下载数量
        max_per_download = input("最多允许每个用户下载多少个文件（回车默认不做限制）：")
        if max_per_download.isdigit():
            os.system(r"sed -i 's/%s/max_per_ip=%s/' %s" % (max_per_ip_info, max_per_download, ftp_file))
        else:
            os.system(r"sed -i 's/%s/max_per_ip=0/' %s" % (max_per_ip_info,ftp_file))

        #Bug需要修复 当开启监听地址时，需要注释掉listen_ipv6选项 不然会报错
        listening = input("是否开启监听地址(y/n/回车默认不开启)：")
        # 开启侦听地址
        if listening.lower() == "y":
            os.system(r"sed -i 's/%s/listen=YES/' %s"%(listen_info,ftp_file))
            # 配置侦听地址
            listening_address = input("请输入监听FTP服务的IP地址（回车默认全网段）：")
            if listening_address == "":
                os.system(r"sed -i 's/%s/listen_address=0.0.0.0/' %s" % (listen_address_info, ftp_file))
            else:
                os.system(
                    r"sed -i 's/%s/listen_address=%s/' %s" % (listen_address_info, listening_address, ftp_file))

            listening_port = input("请输入监听FTP服务的端口号（回车端口号默认21号）：")
            if listening_port == "":
                os.system(r"sed -i 's/%s/listen_port=21/' %s" % (listen_port_info, ftp_file))
            else:
                os.system(r"sed -i 's/%s/listen_port=%s/' %s" % (listen_port_info, listening_port, ftp_file))
        # 不开启监听地址
        elif listening.lower() == "n":
            os.system(r"sed -i 's/%s/listen=NO/' %s"%(listen_info,ftp_file))
        # 不开启监听地址
        else:
            os.system(r"sed -i 's/%s/listen=NO/' %s" % (listen_info, ftp_file))

        local_ftp_content = open(ftp_file, "r")
        local_ftp_content = local_ftp_content.read()
        with open(ftp_file, "w", encoding="utf-8") as f:
            f.write(local_ftp_content)

    def config_local_users(self):

        # ftp服务主配置文件
        ftp_file = r"/etc/vsftpd/vsftpd.conf"

        # 覆盖原先配置文件
        os.system("\cp -rf ./vsftpd.conf /etc/vsftpd/vsftpd.conf")

        # 本地用户配置项
        local_enable = os.popen("sed -n '/local_enable/p' %s"%ftp_file)
        local_enable_info = local_enable.read().strip()
        local_umask = os.popen("sed -n '/local_umask/p' %s"%ftp_file)
        local_umask_info = local_umask.read().strip()
        local_root = os.popen("sed -n '/local_root/p' %s"%ftp_file)
        local_root_info = local_root.read().strip()
        local_max_rate = os.popen("sed -n '/local_max_rate/p' %s"%ftp_file)
        local_max_rate_info = local_max_rate.read().strip()

        # 配置本地用户访问权限，只能输入y或n，输入其他租房有默认拒绝
        enable_local = input("是否允许本地用户系统访问(y/n/回车默认拒绝)：")
        # 允许本地用户
        if enable_local.lower() == "y":
            os.system("sed -i 's/%s/local_enable=YES/' %s"%(local_enable_info,ftp_file))
            os.system("sed -i 's/%s/local_umask=022/' %s"%(local_umask_info,ftp_file))
            os.system("sed -i 's/%s/local_max_rate=0/' %s"%(local_max_rate_info,ftp_file))

            local_root_path = input("请输入本地用户的根目录（回车默认设置为/var/ftp）：")
            if local_root_path == "":
                os.system("sed -i 's/%s/local_root=\/var\/ftp/' %s" % (local_root_info.replace("/", "\/"), ftp_file))
            else:
                os.system("sed -i 's/%s/local_root=%s/' %s" % (
                local_root_info.replace("/", "\/"), local_root_path.replace("/", "\/"), ftp_file))
        # 拒绝本地用户
        elif enable_local.lower() == "n":
            os.system("sed -i 's/%s/local_enable=NO/' %s"%(local_enable_info,ftp_file))
            os.system("sed -i 's/%s/#local_umask=022/' %s" % (local_umask_info, ftp_file))
            os.system("sed -i '/local_root/s/%s/#%s/g' %s"%(local_root_info.replace("/","\/"), local_root_info.replace("/","\/"), ftp_file))
            os.system("sed -i 's/%s/#local_max_rate=0/' %s" % (local_max_rate_info, ftp_file))
        # 拒绝本地用户
        else:
            os.system("sed -i 's/%s/local_enable=NO/' %s" % (local_enable_info, ftp_file))
            os.system("sed -i 's/%s/#local_umask=022/' %s" % (local_umask_info, ftp_file))
            os.system("sed -i '/local_root/s/%s/#%s/g' %s" % (
            local_root_info.replace("/", "\/"), local_root_info.replace("/", "\/"), ftp_file))
            os.system("sed -i 's/%s/#local_max_rate=0/' %s" % (local_max_rate_info, ftp_file))

        local_ftp_content = open(ftp_file, "r")
        local_ftp_content = local_ftp_content.read()
        with open(ftp_file, "w", encoding="utf-8") as f:
            f.write(local_ftp_content)

        global_config = input("是否进入全局配置(y/n)：")
        if global_config.lower() == "y":
            self.global_config()
        else:
            pass

