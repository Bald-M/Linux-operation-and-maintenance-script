# -*- coding:UTF-8 -*-
# 作者：张子涵
# https://github.com/Bald-M/Linux-operation-and-maintenance-script

import os,re

class Config_HTTP():
    def __init__(self):
        pass
    def backup(self):
        if not os.path.exists("/backup"):
            if not os.path.exists("/etc/httpd/conf/httpd.conf"):
                info = "系统未检测到httpd服务，请安装！"
                return info

            else:
                os.mkdir("/backup")
                os.system("cp -rf /etc/httpd/conf/httpd.conf /backup")

        else:
            if not os.path.exists("/etc/httpd/conf/httpd.conf"):
                info = "系统未检测到httpd服务，请安装！"
                return info

            else:
                os.system("cp -rf /etc/httpd/conf/httpd.conf /backup")

    def write_in_file(self,file_path,content,mode):
        with open(file_path,mode,encoding="utf-8") as f:
            f.write(content)

    def clients_address_restrictions(self):
        # http服务主配置文件
        http_file = r"/etc/httpd/conf/httpd.conf"
        # 本地http服务主配置文件
        local_http_file = open("./httpd.conf","r")
        contents = local_http_file.read()

        # 客户机地址限制配置项
        example_require_all_granted = re.findall("Require all granted",contents)
        example_require_all_granted = example_require_all_granted[1]

        example_require_ip = re.findall("#Require ip .*",contents)
        example_require_ip = example_require_ip[0]

        example_require_not_ip = re.findall("#Require not ip .*",contents)
        example_require_not_ip = example_require_not_ip[0]


        require_all_granted = input("是否允许所有主机访问(y/n/回车默认拒绝)：")
        # 允许所有主机访问
        if require_all_granted.lower() == "y":
            # Require not ip 192.168.0.0/24 192.168.1.2 有子网掩码则拒绝网段，没有就拒绝单一主机
            require_not_ip = input("请输入仅拒绝的ip地址或网段（没有则按回车）：")
            if require_not_ip == "":
                self.write_in_file(http_file,contents,"w")
            # 仅拒绝主机或网段访问，前面需要添加Require all granted
            else:
                replace_content = contents.replace(example_require_not_ip,"Require not ip %s"%require_not_ip)
                self.write_in_file(http_file,replace_content,"w")

        # 拒绝所有主机访问
        elif require_all_granted.lower() == 'n':
            # Require ip 192.168.0.0/24 192.168.1.2 有子网掩码则允许网段，没有就允许单一主机
            require_ip = input("请输入仅允许的ip地址或网段（没有则按回车）：")
            # Requir all granted = Require all denied
            if require_ip == "":
                replace_content = contents.replace(example_require_all_granted,"Require all denied")
                self.write_in_file(http_file,replace_content,"w")
            # 仅允许主机或网段访问，前面不需要添加Require all denied
            else:
                replace_content = contents.replace(example_require_all_granted, "#"+example_require_all_granted).replace(example_require_ip,"Require ip %s"%require_ip)
                self.write_in_file(http_file,replace_content,"w")

        # 拒绝所有主机访问
        else:
            # Require ip 192.168.0.0/24 192.168.1.2 有子网掩码则允许网段，没有就允许单一主机
            require_ip = input("请输入仅允许的ip地址或网段（没有则按回车）：")
            if require_ip == "":
                replace_content = contents.replace(example_require_all_granted, "Require all denied")
                self.write_in_file(http_file, replace_content, "w")

            else:
                replace_content = contents.replace(example_require_all_granted,
                                                   "#" + example_require_all_granted).replace(example_require_ip,
                                                                                              "Require ip %s" % require_ip)
                self.write_in_file(http_file, replace_content, "w")



    def users_authentication_restriction(self):
        # http服务的主配置文件
        http_file = r"/etc/httpd/conf/httpd.conf"
        # 本地http服务配置文件
        local_http_file = open("./httpd.conf", "r")
        contents = local_http_file.read()

        # 用户认证配置项
        user_auth_config = re.findall('''	#AuthName .*
    #AuthType .*
    #AuthUserFile .*
    #Require .*'''.strip(),contents)
        user_auth_config = user_auth_config[0]

        client_limit_config = re.findall('''<RequireAll>
		Require all .*
		#Require ip .*
		#Require not .*
	</RequireAll>'''.strip(),contents)
        client_limit_config = client_limit_config[0]

        # 输入其他字符或者n则默认不开启
        user_auth_restriction = input("是否开启用户授权限制(y/n/回车默认不开启)：")
        # 开启用户授权
        if user_auth_restriction.lower() == "y":
            username = input("请输入用户名：")
            # 如果/etc/httpd/conf/.awspwd不存在则添加-c选项，存在则不添加
            if not os.path.exists("/etc/httpd/conf/.awspwd"):
                os.system("/usr/bin/htpasswd -c /etc/httpd/conf/.awspwd %s" % username)
                replace_content = contents.replace(user_auth_config, user_auth_config.replace("#", "")).replace(
                    client_limit_config, "")
                self.write_in_file(http_file, replace_content, "w")
            else:
                os.system("/usr/bin/htpasswd  /etc/httpd/conf/.awspwd %s" % username)
                replace_content = contents.replace(user_auth_config, user_auth_config.replace("#", "")).replace(
                    client_limit_config, "")
                self.write_in_file(http_file, replace_content, "w")
        # 不开启用户授权
        elif user_auth_restriction.lower() == "n":
            pass
        # 不开启用户授权
        else:
            pass


class Config_virtual_host():
    def __init__(self):
        pass
    def based_on_domain_name(self):
        pass
    def based_on_ip_address(self):
        use_write_func = Config_HTTP()

        # 本地http服务主配置文件
        local_http_file = open("./httpd.conf","r")
        content = local_http_file.read()
        # 本地虚拟主机配置文件
        local_vhosts_file = open("./httpd-vhosts.conf", "r")
        contents = local_vhosts_file.read()

        # 导入独立的配置文件
        include = re.findall("#Include /etc/httpd/conf/extra/httpd-vhosts.conf",content)
        include = include[0]

        # 虚拟主机（基于IP）配置项
        virtualhost_ip = re.findall("#<VirtualHost (.*):80>",contents)
        virtualhost_ip = virtualhost_ip[0]
        virtualhost_doc = re.findall('DocumentROOT "(.*)"',contents)
        virtualhost_doc = virtualhost_doc[0]
        virtualhost_config = re.findall('''#<VirtualHost .*:80>
#        DocumentROOT ".*"
#</VirtualHost>'''.strip(),contents)
        virtualhost_config = virtualhost_config[0]


        num_ip = input("请输入你的ip数量：")
        for i in range(1, int(num_ip) + 1):
            ip_addr = input("请输入ip地址：")
            document_root = input("请输入网页所在路径：")
            # 如果虚拟主机配置文件不存在，则创建/etc/httpd/conf/extra/httpd-vhosts.conf，否则就不创建
            if not os.path.exists('/etc/httpd/conf/extra/httpd-vhosts.conf'):
                os.system("mkdir -p /etc/httpd/conf/extra")
                replace_contents = virtualhost_config.replace("#", "").replace(virtualhost_ip, ip_addr).replace(
                    virtualhost_doc, document_root)
                use_write_func.write_in_file("/etc/httpd/conf/extra/httpd-vhosts.conf",replace_contents+'\n',"a")
                replace_content = content.replace(include,"Include /etc/httpd/conf/extra/httpd-vhosts.conf")
                use_write_func.write_in_file("/etc/httpd/conf/httpd.conf",replace_content,"w")
            else:
                replace_contents = virtualhost_config.replace("#", "").replace(virtualhost_ip, ip_addr).replace(
                    virtualhost_doc, document_root)
                use_write_func.write_in_file('/etc/httpd/conf/extra/httpd-vhosts.conf', replace_contents + '\n',
                                             'a')
                replace_content = content.replace(include, "Include /etc/httpd/conf/extra/httpd-vhosts.conf")
                use_write_func.write_in_file("/etc/httpd/conf/httpd.conf", replace_content, "w")


    def based_on_port(self):
        use_write_func = Config_HTTP()

        # 本地http服务主配置文件
        local_http_file = open("./httpd.conf", "r")
        content = local_http_file.read()
        # 本地虚拟主机配置文件
        local_vhosts_file = open("./httpd-vhosts.conf", "r")
        contents = local_vhosts_file.read()

        # 导入独立的配置文件
        include = re.findall("#Include /etc/httpd/conf/extra/httpd-vhosts.conf", content)
        include = include[0]

        # 虚拟主机（基于端口）配置项
        virtualhost_ip = re.findall("#<VirtualHost (.*):80>", contents)
        virtualhost_ip = virtualhost_ip[0]
        virtualhost_port = re.findall("#<VirtualHost .*:(80)>", contents)
        virtualhost_port = virtualhost_port[0]
        virtualhost_doc = re.findall('DocumentROOT "(.*)"', contents)
        virtualhost_doc = virtualhost_doc[0]
        virtualhost_config = re.findall('''#<VirtualHost .*>
#        DocumentROOT .*
#</VirtualHost>'''.strip(), contents)
        virtualhost_config = virtualhost_config[0]
        # 删除旧侦听端口
        os.system("sed -i '367,10000d' /etc/httpd/conf/httpd.conf")
        ip_addr = input("请输入ip地址：")
        num_port = input("请输入端口的数量：")
        for i in range(1 , int(num_port) + 1):
            port = input("请输入端口号：")
            document_root = input("请输入网页所在路径：")
            if not os.path.exists('/etc/httpd/conf/extra/httpd-vhosts.conf'):
                os.system("mkdir -p /etc/httpd/conf/extra")

                replace_contents = virtualhost_config.replace("#", "").replace(virtualhost_port,port).replace(
                    virtualhost_doc, document_root).replace(virtualhost_ip,ip_addr)
                use_write_func.write_in_file("/etc/httpd/conf/extra/httpd-vhosts.conf", replace_contents + "\n", "a")
                #添加新端口
                use_write_func.write_in_file("/etc/httpd/conf/httpd.conf","Listen %s\n"%port,"a")

            else:
                replace_contents = virtualhost_config.replace("#", "").replace(
                    virtualhost_port, port).replace(
                    virtualhost_doc, document_root).replace(virtualhost_ip,ip_addr)
                use_write_func.write_in_file("/etc/httpd/conf/extra/httpd-vhosts.conf", replace_contents + "\n", "a")
                use_write_func.write_in_file("/etc/httpd/conf/httpd.conf", "Listen %s\n" % port, "a")











