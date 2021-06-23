import os
class Configure_FTP():
    def __init__(self):
        pass

    def backup(self):

        if not os.path.exists('/backup'):
            if not os.path.exists('/etc/vsftpd/vsftpd.conf'):
                info = "系统未检测到vsftpd服务，请安装！"
                return info

            # if os.path.exists('/etc/vsftpd/vsftpd.conf'):
            #     os.mkdir('/backup')
            #     os.system('cp -rf /etc/vsftpd/vsftpd.conf /backup')
            else:
                os.mkdir('/backup')
                os.system('cp -rf /etc/vsftpd/vsftpd.conf /backup')

        else:
            if not os.path.exists('/etc/vsftpd/vsftpd.conf'):
                info = "系统未检测到vsftpd服务，请安装！"
                return info

            # if os.path.exists('/etc/vsftpd/vsftpd.conf'):
            #     os.system('cp -rf /etc/vsftpd/vsftpd.conf /backup')
            else:
                os.system('cp -rf /etc/vsftpd/vsftpd.conf /backup')



    def config_anonymous_users(self):
        file_path = r'/etc/vsftpd/vsftpd.conf'
        ftp_file = r'./vsftpd.conf'

        allow_anonymous = input("是否允许匿名用户(y-n)：")
        #匿名用户配置项
        anon_enable = os.popen(r"sed -n '/anonymous_enable/p' %s "%ftp_file)
        anon_enable_info = anon_enable.read().strip()
        anon_umask = os.popen(r"sed -n '/anon_umask/p' %s"%ftp_file)
        anon_umask_info = anon_umask.read().strip()
        anon_root = os.popen(r"sed -n '/anon_root/p' %s"%ftp_file)
        anon_root_info = anon_root.read().strip()
        anon_upload_enable = os.popen(r"sed -n '/anon_upload_enable/p' %s"%ftp_file)
        anon_upload_enable_info = anon_upload_enable.read().strip()
        anon_mkdir_write_enable = os.popen(r"sed -n '/anon_mkdir_write_enable/p' %s"%ftp_file)
        anon_mkdir_write_enable_info = anon_mkdir_write_enable.read().strip()
        anon_other_write_enable = os.popen(r"sed -n '/anon_other_write_enable/p' %s"%ftp_file)
        anon_other_write_enable_info = anon_other_write_enable.read().strip()
        anon_max_rate = os.popen(r"sed -n '/anon_max_rate/p' %s "%ftp_file)
        anon_max_rate_info = anon_max_rate.read().strip()

        if allow_anonymous.lower() == 'y':
            #允许匿名访问
            os.system(r"sed -i 's/%s/anonymous_enable=YES/' %s"%(anon_enable_info,ftp_file))

            anon_umask_config = input("请输入匿名用户所上传文件的默认权限掩码值：")
            if anon_umask_config == '':
                os.system(r"sed -i 's/%s/anon_umask=022/' %s " % (anon_umask_info, ftp_file))
            else:
                os.system(r"sed -i 's/%s/anon_umask=%s/' %s " % (anon_umask_info,anon_umask_config, ftp_file))

            anon_root_path = input("请输入匿名用户的根目录:")
            if anon_root_path =='':
                #设置匿名用户根目录（/var/ftp）
                os.system(r"sed -i '/anon_root/s/%s/anon_root=\/var\/ftp/g' %s"%(anon_root_info.replace("/","\/"),ftp_file))
                #sed -i '/anon_root/s/anon_root=\/root/anon_root=\/zzh/g' vsftpd.conf
            else:
                # 设置匿名用户根目录（用户自定义）
                os.system(r"sed -i '/anon_root/s/%s/anon_root=%s/g' %s"%(anon_root_info.replace("/","\/"),anon_root_path.replace("/","\/"),ftp_file))

            #匿名用户上传控制
            enable_anon_upload = input("是否允许匿名用户上传文件(y-n)：")
            if enable_anon_upload.lower() == 'y':
                #允许匿名用户上传文件
                os.system("sed -i '/anon_upload_enable/s/%s/anon_upload_enable=YES/g' %s "%(anon_upload_enable_info.replace("/","\/"),ftp_file))
            elif enable_anon_upload.lower() == 'n':
                #禁止匿名用户上传文件
                os.system("sed -i '/anon_upload_enable/s/%s/anon_upload_enable=NO/g' %s "%(anon_upload_enable_info.replace("/","\/"),ftp_file))
                #sed -i '/anon_upload_enable/s/#anon_upload_enable=YES/anon_upload_enable=NO/g' vsftpd.conf

            #匿名用户创建文件控制
            anon_mkdir_write = input("是否允许匿名用户创建文件(y-n)：")
            if anon_mkdir_write.lower() == 'y':
                os.system("sed -i '/anon_mkdir_write_enable/s/%s/anon_mkdir_write_enable=YES/g' %s "%(anon_mkdir_write_enable_info.replace("/","\/"),ftp_file))
            elif anon_mkdir_write.lower() == 'n':
                os.system("sed -i '/anon_mkdir_write_enable/s/%s/anon_mkdir_write_enable=NO/g' %s "%(anon_mkdir_write_enable_info.replace("/","\/"),ftp_file))

            #匿名用户其他写入权限
            anon_other_write_enable = input("是否允许匿名用户有其他写入权限，如对文件改名、覆盖及删除文件等(y-n)：")
            if anon_other_write_enable.lower() == 'y':
                os.system("sed -i '/anon_other_write_enable/s/%s/anon_other_write_enable=YES/g' %s "%(anon_other_write_enable_info.replace("/","\/"),ftp_file))
            elif anon_other_write_enable.lower() == 'n':
                os.system("sed -i '/anon_other_write_enable/s/%s/anon_other_write_enable=NO/g' %s "%(anon_other_write_enable_info.replace("/","\/"),ftp_file))

            anon_max_rate_config = input("请输入最大传输速率（0代表无限制）：")
            if anon_max_rate_config == '':
                os.system(r"sed -i 's/%s/anon_max_rate=0/' %s " % (anon_max_rate_info, ftp_file))
            else:
                os.system(r"sed -i 's/%s/anon_max_rate=%s/' %s " % (anon_max_rate_info,anon_max_rate_config, ftp_file))

        elif allow_anonymous.lower() == 'n':
            os.system(r"sed -i 's/%s/anonymous_enable=NO/' %s" % (anon_enable_info,ftp_file))
            #anon_umask
            os.system(r"sed -i 's/%s/#anon_umask=022/' %s " % (anon_umask_info, ftp_file))
            #anon_root
            os.system(r"sed -i 's/%s/#%s/' %s"%(anon_root_info.replace("/","\/"),anon_root_info.replace("/","\/"),ftp_file))
            #anon_upload
            os.system(r"sed -i 's/%s/#%s/' %s"%(anon_upload_enable_info.replace("/","\/"),anon_upload_enable_info.replace("/","\/"),ftp_file))
            #anon_mkdir_write
            os.system(r"sed -i 's/%s/#%s/' %s" % (
            anon_mkdir_write_enable_info.replace("/", "\/"), anon_mkdir_write_enable_info.replace("/", "\/"), ftp_file))
            #anon_other_write
            os.system(r"sed -i 's/%s/#%s/' %s" % (
                anon_other_write_enable_info.replace("/", "\/"), anon_other_write_enable_info.replace("/", "\/"),
                ftp_file))
            #anon_max_rate
            os.system(r"sed -i 's/%s/#%s/' %s " % (anon_max_rate_info.replace("/","\/"),anon_max_rate_info.replace("/","\/"),ftp_file))


        local_ftp_content = open(ftp_file,'r')
        local_ftp_content = local_ftp_content.read()
        with open(file_path,'w',encoding='utf-8') as f:
            f.write(local_ftp_content)

    def global_config(self):

        file_path = r'/etc/vsftpd/vsftpd.conf'
        ftp_file = r'./vsftpd.conf'

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

        enable_write = input("是否启用任何形式的写入权限（如上传、删除文件等）都需要开启此选项(y-n)：")
        if enable_write.lower() == 'y':
            os.system(r"sed -i 's/%s/write_enable=YES/' %s" % (write_enable_info, ftp_file))
        elif enable_write.lower() == 'n':
            os.system(r"sed -i 's/%s/write_enable=NO/' %s" % (write_enable_info, ftp_file))

        enable_download = input("是否允许下载文件（建立仅限于浏览、上传的FTP服务器时可将其设为No）(y-n)：")
        if enable_download.lower() == 'y':
            os.system(r"sed -i 's/%s/download_enable=YES/' %s"%(download_enable_info,ftp_file))
        elif enable_download.lower() == 'n':
            os.system(r"sed -i 's/%s/download_enable=NO/' %s"%(download_enable_info,ftp_file))

        enable_userlist = input("是否启用user_list用户列表文件(y-n)：")
        if enable_userlist.lower() == 'y':
            os.system(r"sed -i 's/%s/userlist_enable=YES/' %s"%(userlist_enable_info,ftp_file))
        elif enable_userlist.lower() == 'n':
            os.system(r"sed -i 's/%s/userlist_enable=NO/' %s"%(userlist_enable_info,ftp_file))

        deny_userlist = input("是否禁止user_list列表文件中的用户账号(y-n)：")
        if deny_userlist.lower() == 'y':
            os.system(r"sed -i 's/%s/userlist_deny=YES/' %s"%(userlist_deny_info,ftp_file))
        elif deny_userlist.lower() == 'n':
            os.system(r"sed -i 's/%s/userlist_deny=NO/' %s"%(userlist_deny_info,ftp_file))

        max_connection = input("最多允许多少用户同时登录：")
        if max_connection.isdigit():
            os.system(r"sed -i 's/%s/max_clients=%s/' %s" % (max_clients_info, max_connection, ftp_file))
        else:
            os.system(r"sed -i 's/%s/max_clients=0/' %s"%(max_clients_info,ftp_file))

        max_per_download = input("最多允许每个用户下载多少个文件：")
        if max_per_download.isdigit():
            os.system(r"sed -i 's/%s/max_per_ip=%s/' %s" % (max_per_ip_info, max_per_download, ftp_file))
        else:
            os.system(r"sed -i 's/%s/max_per_ip=0/' %s" % (max_per_ip_info,ftp_file))

        listening = input("是否开启监听地址(y-n)：")
        if listening.lower() == 'y':
            os.system(r"sed -i 's/%s/listen=YES/' %s"%(listen_info,ftp_file))

            listening_address = input("请输入监听FTP服务的IP地址：")
            if listening_address != '':
                os.system(r"sed -i 's/%s/listen_address=%s/' %s" % (listen_address_info, listening_address, ftp_file))
            else:
                os.system(r"sed -i 's/%s/listen_address=0.0.0.0/' %s" % (listen_address_info, ftp_file))

            listening_port = input("请输入监听FTP服务的端口号：")
            if listening_port != '':
                os.system(r"sed -i 's/%s/listen_port=%s/' %s" % (listen_port_info, listening_port,ftp_file))
            else:
                os.system(r"sed -i 's/%s/listen_port=21/' %s" % (listen_port_info, ftp_file))

        elif listening.lower() == 'n':
            os.system(r"sed -i 's/%s/listen=NO/' %s"%(listen_info,ftp_file))

        local_ftp_content = open(ftp_file, 'r')
        local_ftp_content = local_ftp_content.read()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(local_ftp_content)

    def config_local_users(self):
        file_path = r'/etc/vsftpd/vsftpd.conf'
        ftp_file = r'./vsftpd.conf'

        local_enable = os.popen("sed -n '/local_enable/p' %s"%ftp_file)
        local_enable_info = local_enable.read().strip()
        local_umask = os.popen("sed -n '/local_umask/p' %s"%ftp_file)
        local_umask_info = local_umask.read().strip()
        local_root = os.popen("sed -n '/local_root/p' %s"%ftp_file)
        local_root_info = local_root.read().strip()
        local_max_rate = os.popen("sed -n '/local_max_rate/p' %s"%ftp_file)
        local_max_rate_info = local_max_rate.read().strip()

        enable_local = input("是否允许本地用户系统访问(y-n)：")
        if enable_local.lower() == 'y':
            os.system("sed -i 's/%s/local_enable=YES/' %s"%(local_enable_info,ftp_file))
            os.system("sed -i 's/%s/local_umask=022/' %s"%(local_umask_info,ftp_file))
            os.system("sed -i 's/%s/local_max_rate=0/' %s"%(local_max_rate_info,ftp_file))

            local_root_path = input("请输入本地用户的根目录：")
            if local_root_path == '':
                os.system("sed -i 's/%s/local_root=\/var\/ftp/' %s" % (local_root_info.replace("/", "\/"), ftp_file))
            else:
                os.system("sed -i 's/%s/local_root=%s/' %s" % (
                local_root_info.replace("/", "\/"), local_root_path.replace("/", "\/"), ftp_file))

        elif enable_local.lower() == 'n':
            os.system("sed -i 's/%s/local_enable=NO/' %s"%(local_enable_info,ftp_file))
            os.system("sed -i 's/%s/#local_umask=022/' %s" % (local_umask_info, ftp_file))
            os.system("sed -i '/local_root/s/%s/#%s/g' %s"%(local_root_info.replace("/","\/"), local_root_info.replace("/","\/"), ftp_file))
            os.system("sed -i 's/%s/#local_max_rate=0/' %s" % (local_max_rate_info, ftp_file))

        local_ftp_content = open(ftp_file, 'r')
        local_ftp_content = local_ftp_content.read()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(local_ftp_content)

        global_config = input("是否进入全局配置(y-n)：")
        if global_config.lower() == 'y':
            self.global_config()
        else:
            pass

    def select_mode(self):
        print("(1)配置匿名用户\n(2)配置本地用户\n(3)我全都要")
        select = int(input("请选择配置选项："))
        if select == 1:
            self.config_anonymous_users()
        elif select == 2:
            self.config_local_users()
        elif select == 3:
            self.config_anonymous_users()
            self.config_local_users()
