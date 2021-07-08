# -*- coding:UTF-8 -*-
# 作者：张子涵
# https://github.com/Bald-M/Linux-operation-and-maintenance-script

import os,re

class Configure_DHCP():
    def __init__(self):
        pass
    # 函数 备份
    def backup(self):
        # 检测/backup目录是否存在，存在则不创建，不存在则创建/backup
        # 检测/etc/dhcp/dhcpd.conf目录是否存在，不存在则提示系统未安装dhcpd服务
        if not os.path.exists("/backup"):
            if not os.path.exists("/etc/dhcp/dhcpd.conf"):
                info = "系统未检测到dhcpd服务，请安装！"
                return info

            else:
                # 将源配置文件/usr/share/doc/dhcp*/dhcpd.conf.example备份到/backup目录下
                # 当启动服务报错则可以还原
                os.mkdir("/backup")
                os.system("cp -rf /usr/share/doc/dhcp*/dhcpd.conf.example /backup")

        else:
            if not os.path.exists("/etc/dhcp/dhcpd.conf"):
                info = "系统未检测到dhcpd服务，请安装！"
                return info

            else:
                # 当/backup目录已存在，程序则不会创建/backup目录
                # 程序直接开始备份
                os.system("cp -rf /usr/share/doc/dhcp*/dhcpd.conf.example /backup")

    # 函数 建立主配置文件
    def build_main_file(self):
        # dhcp_file指的是dhcp主配置文件的路径
        dhcp_file = r"/etc/dhcp/dhcpd.conf"

        # cp前面加\表示不会提示任何信息
        # 这里将dhcp模板的文件拷贝到主配置文件方便配置
        os.system(r"\cp /usr/share/doc/dhcp*/dhcpd.conf.example %s" % dhcp_file)

        # 下面的思路是使用正则表达式匹配我们所需要更改的配置项，
        # 用replace函数将我们输入的值替换本地配置文件的值并保存在变量replace_content里
        # （replace函数只会在内存进行替换，不会写入到本地配置文件）
        # 最后将变量replace_content写入到dhcp主配置文件中

        # local_dhcp_file指的是本地dhcp配置文件
        local_dhcp_file = open("./dhcpd.conf", "r")
        contents = local_dhcp_file.read()

        # 本地配置文件域名模板
        example_domain_name = re.findall("option domain-name (.*);", contents)

        # 本地配置文件DNS模板
        example_domain_name_server = re.findall("option domain-name-servers (.*);", contents)

        # 本地配置文件网段模板
        example_subnet = re.findall("subnet (.*) netmask .*", contents)

        # 本地配置文件子网掩码模板
        example_netmask = re.findall("subnet .* netmask ([0-9.]*|[0-9]*)", contents)

        # 本地配置文件DHCP网段范围模板
        config_range_ip = re.findall("range (.*);", contents)
        config_option_router = re.findall("option routers (.*);", contents)

        # 本地配置文件MAC地址模板
        config_hardware_ethernet = re.findall("hardware ethernet (.*);",contents)
        # 本地配置文件预留地址模板
        config_fixed_address = re.findall("fixed-address (.*);",contents)

        example_host_prtsvr = re.findall('''host prtsvr {
    hardware ethernet .*;
    fixed-address .*;
}''',contents)

        # 替换
        while True:
            # 设置域名
            domain_name = input("请输入你的域名：")
            # 域名使用双引号包裹 "domain_name"
            domain_name = "\"%s\"" % domain_name
            # 设置DNS，没有DNS可填网关
            domain_name_server = input("请输入你的DNS：")
            # 设置网段
            subnet = input("请输入你的subnet网段：")
            # 设置子网掩码
            netmask = input("请输入你的子网掩码：")
            # 设置分配地址范围 192.168.1.100 192.168.1.200
            range_ip = input("请输入你要分配IP地址的范围：")
            # 设置网关
            option_router = input("请输入你的默认网关地址：")
            # 输入y或n（不区分大小写），如果输入其他字符则不设置预留地址，输入回车则提示不能输入空值
            reserved_address = input("是否设置预留地址(y/n)：")
            if domain_name == "" or domain_name_server == "" or subnet == "" or netmask == "" or range_ip == "" or option_router == "" or reserved_address == "":
                print("你不能输入空值！")

            # 如果不设置预留地址，则注释预留地址模板
            elif reserved_address.lower() == "n":
                replace_content = contents.replace(example_domain_name[0], domain_name).replace(
                    example_domain_name_server[0], domain_name_server).replace(example_subnet[0], subnet).replace(
                    example_netmask[0], netmask).replace(config_range_ip[0], range_ip).replace(config_option_router[0],
                                                                                               option_router).replace(example_host_prtsvr[0],"")
                with open(dhcp_file,"w",encoding="utf-8") as f:
                    f.write(replace_content)
                    break
            elif reserved_address.lower() == "y":
                hardware_ethernet = input("请输入目标主机的MAC地址：")
                fixed_address = input("请输入预留地址：")
                replace_content = contents.replace(example_domain_name[0], domain_name).replace(
                    example_domain_name_server[0], domain_name_server).replace(example_subnet[0], subnet).replace(
                    example_netmask[0], netmask).replace(config_range_ip[0], range_ip).replace(config_option_router[0],
                                                                                               option_router).replace(config_hardware_ethernet[0],hardware_ethernet.replace("-",":")).replace(config_fixed_address[0],fixed_address)
                with open(dhcp_file,"w",encoding="utf-8") as f:
                    f.write(replace_content)
                    break
            else:
                replace_content = contents.replace(example_domain_name[0], domain_name).replace(
                    example_domain_name_server[0], domain_name_server).replace(example_subnet[0], subnet).replace(
                    example_netmask[0], netmask).replace(config_range_ip[0], range_ip).replace(config_option_router[0],
                                                                                               option_router).replace(
                    example_host_prtsvr[0], "")
                with open(dhcp_file, "w", encoding="utf-8") as f:
                    f.write(replace_content)
                    break

