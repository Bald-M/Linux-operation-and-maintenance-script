import os,re

class Configure_DHCP():
    def __init__(self):
        pass
    def backup(self):

        if not os.path.exists('/backup'):
            if not os.path.exists('/etc/dhcp/dhcpd.conf'):
                info = "系统未检测到dhcpd服务，请安装！"
                return info

            # if os.path.exists('/etc/dhcp/dhcpd.conf'):
            #     os.mkdir('/backup')
            #     os.system('cp -rf /etc/dhcp/dhcpd.conf /backup')
            else:
                os.mkdir('/backup')
                os.system('cp -rf /etc/dhcp/dhcpd.conf /backup')

        else:
            if not os.path.exists('/etc/dhcp/dhcpd.conf'):
                info = "系统未检测到dhcpd服务，请安装！"
                return info
            # if os.path.exists('/etc/dhcp/dhcpd.conf'):
            #     os.system('cp -rf /etc/dhcp/dhcpd.conf /backup')
            else:
                os.system('cp -rf /etc/dhcp/dhcpd.conf /backup')


    def build_main_file(self):
        file_path = r"/etc/dhcp/dhcpd.conf"

        os.system(r"\cp /usr/share/doc/dhcp*/dhcpd.conf.example %s" % file_path)

        dhcp_file = open('./dhcpd.conf', "r")
        contents = dhcp_file.read()
        # 设置域名 ;
        example_domain_name = re.findall('option domain-name (.*);', contents)

        # 设置DNS ;
        example_domain_name_server = re.findall("option domain-name-servers (.*);", contents)

        # 设置网段
        example_subnet = re.findall("subnet (.*) netmask .*", contents)

        # 设置子网掩码
        example_netmask = re.findall("subnet .* netmask ([0-9.]*|[0-9]*)", contents)

        # 设置DHCP网段
        config_range_ip = re.findall("range (.*);", contents)
        config_option_router = re.findall("option routers (.*);", contents)

        # 设置预留地址
        config_hardware_ethernet = re.findall("hardware ethernet (.*);",contents)
        config_fixed_address = re.findall("fixed-address (.*);",contents)
        example_host_prtsvr = re.findall('''host prtsvr {
    hardware ethernet .*;
    fixed-address .*;
}''',contents)

        # 替换
        while True:
            domain_name = input("请输入你的域名：")
            domain_name = "\"%s\"" % domain_name
            domain_name_server = input("请输入你的DNS：")
            subnet = input("请输入你的subnet网段：")
            netmask = input("请输入你的子网掩码：")

            range_ip = input("请输入你要分配IP地址的范围：")
            option_router = input("请输入你的默认网关地址：")
            reserved_address = input("是否设置预留地址(y-n)：")
            if domain_name == '' or domain_name_server == '' or subnet == '' or netmask == '' or range_ip == '' or option_router == '' or reserved_address == '':
                print("你不能输入空值！")
            elif reserved_address == 'n':
                replace_content = contents.replace(example_domain_name[0], domain_name).replace(
                    example_domain_name_server[0], domain_name_server).replace(example_subnet[0], subnet).replace(
                    example_netmask[0], netmask).replace(config_range_ip[0], range_ip).replace(config_option_router[0],
                                                                                               option_router).replace(example_host_prtsvr[0],'')
                with open(file_path,'w',encoding="utf-8") as f:
                    f.write(replace_content)
                    break
            elif reserved_address == 'y':
                hardware_ethernet = input("请输入目标主机的MAC地址：")
                fixed_address = input("请输入预留地址：")
                replace_content = contents.replace(example_domain_name[0], domain_name).replace(
                    example_domain_name_server[0], domain_name_server).replace(example_subnet[0], subnet).replace(
                    example_netmask[0], netmask).replace(config_range_ip[0], range_ip).replace(config_option_router[0],
                                                                                               option_router).replace(config_hardware_ethernet[0],hardware_ethernet.replace("-",":")).replace(config_fixed_address[0],fixed_address)
                with open(file_path,'w',encoding="utf-8") as f:
                    f.write(replace_content)
                    break
            else:
                replace_content = contents.replace(example_domain_name[0], domain_name).replace(
                    example_domain_name_server[0], domain_name_server).replace(example_subnet[0], subnet).replace(
                    example_netmask[0], netmask).replace(config_range_ip[0], range_ip).replace(config_option_router[0],
                                                                                               option_router).replace(
                    example_host_prtsvr[0], '')
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(replace_content)
                    break

