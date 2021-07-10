# -*- coding:UTF-8 -*-
# 作者：张子涵
# 开始时间：2021/6/16
# https://github.com/Bald-M/service-management-and-control/blob/main/RUN.py

import os
from config_local_yum import local_yum
from DHCP import *
from FTP import *
from HTTP import *

#函数 开启服务
def start_service(service):
    os.system("sudo systemctl start %s"%service)
    return start_service

#函数 关闭服务
def stop_service(service):
    os.system("sudo systemctl stop %s"%service)
    return stop_service

#函数 重启服务
def restart_service(service):
    os.system("sudo systemctl restart %s"%service)
    return restart_service

#函数 查看服务状态
def status_service(service):
    os.system("sudo systemctl status %s"%service)
    return status_service

#函数 开启SELinux
def start_SELinux():
    os.system("sudo setenforce 1")
    print("您已开启SELinux!")

#函数 关闭SELINUX
def stop_SELinux():
    os.system("sudo setenforce 0")
    print("您已关闭SELinux!")

#函数 查看已经开启的服务
def show_services(select):
    if select == 4:
        os.system("sudo systemctl list-unit-files | grep enabled | awk '{print $1}'")
        return show_services
    elif select == 5:
        os.system("sudo systemctl list-unit-files | grep disabled | awk '{print $1}'")
        return show_services

#函数 打印选项列表
def show_select_option():
    print('''
(0)查看服务状态
(1)开启服务
(2)关闭服务
(3)重启服务
(4)查看开启的服务
(5)查看关闭的服务
(6)安装服务或软件
(7)卸载服务或软件
(8)配置本地yum源
(9)配置DHCP
(10)配置FTP
(11)配置HTTP
(20)开启SELinux
(21)关闭SELinux
(100)退出
    '''.strip())
#配置网络yum源
while True:
    show_select_option()
    try:
        # 选择服务，只能输入数字，输入其他字符则会提示输入的字符类型不对
        select = int(input("请选择服务选项:"))
        # 查看服务状态
        if select == 0:
            service = input("请输入服务名称:")
            status_service(service)
        # 开启服务
        elif select == 1:
            service = input("请输入服务名称:")
            start_service(service)
            print("您已开启服务！")
        # 关闭服务
        elif select == 2:
            service = input("请输入服务名称:")
            stop_service(service)
            print("您已关闭服务！")
        # 重启服务
        elif select == 3:
            service = input("请输入服务名称:")
            restart_service(service)
            print("您已重启服务！")
        # 查看开启的服务
        elif select == 4:
            show_services(select)
        # 查看关闭的服务
        elif select == 5:
            show_services(select)
        # 使用yum安装服务
        elif select == 6:
            service = input("请输入服务名称:")
            os.system("yum install %s -y" % service)
        # 使用yum卸载服务
        elif select == 7:
            service = input("请输入服务名称:")
            os.system("yum remove %s -y" % service)

        #配置本地yum源
        elif select == 8:
            local_yum()

        #配置DHCP
        elif select == 9:
            a = Configure_DHCP()
            # 如果未安装dhcpd服务，则会提示未安装信息
            if a.backup() == "系统未检测到dhcpd服务，请安装！":
                print(a.backup())
                continue
            # 如果安装dhcpd服务，则会先备份/usr/share/doc/dhcp*/dhcpd.conf.example到/backup
            else:
                a.backup()
                a.build_main_file()

        #配置vsftpd
        elif select == 10:
            a = Configure_FTP()
            if a.backup() == "系统未检测到vsftpd服务，请安装！":
                print(a.backup())
                continue
            else:
                a.backup()
                while True:
                    print("(1)配置匿名用户\n(2)配置本地用户\n(3)我全都要\n(10)返回主目录")
                    select = int(input("请选择配置选项："))
                    # 配置匿名用户
                    if select == 1:
                        a.config_anonymous_users()
                        continue
                    # 配置本地用户
                    elif select == 2:
                        a.config_local_users()
                        continue
                    # 配置匿名用户和本地用户
                    elif select == 3:
                        a.config_anonymous_users()
                        a.config_local_users()
                        continue
                    # 返回主目录
                    elif select == 10:
                        break



        # 配置HTTP
        elif select == 11:
            a = Config_HTTP()
            b = Config_virtual_host()
            if a.backup() == "系统未检测到httpd服务，请安装！":
                print(a.backup())
                continue
            else:
                a.backup()
                while True:
                    print("(1)客户机地址限制\n(2)用户授权限制\n(3)确认用户数据文件\n(4)删除用户账号\n(5)虚拟主机（基于IP地址）\n(6)虚拟主机（基于端口）\n(10)返回主目录")
                    select = int(input("请选择服务选项:"))
                    #配置客户机地址限制
                    if select == 1:
                        if os.path.exists("/etc/httpd/conf.d/welcome.conf"):
                            # 备份欢迎信息
                            os.system("mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.bak")
                            a.backup()
                            a.clients_address_restrictions()
                            continue
                        else:
                            a.backup()
                            a.clients_address_restrictions()
                            continue
                    #配置用户认证
                    elif select == 2:
                        if os.path.exists("/etc/httpd/conf.d/welcome.conf"):
                            # 备份欢迎信息
                            os.system("mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.bak")
                            a.backup()
                            a.users_authentication_restriction()
                            continue
                        else:
                            a.backup()
                            a.users_authentication_restriction()
                            continue
                    #打印用户认证信息
                    elif select == 3:
                        os.system("cat /etc/httpd/conf/.awspwd")
                        print("您的用户数据保存在/etc/httpd/conf/.awspwd路径下")
                        continue
                    #删除用户账号
                    elif select == 4:
                        username = input("请输入用户名：")
                        os.system("sed -i '/%s/d' /etc/httpd/conf/.awspwd "%username)
                        continue
                    #配置虚拟主机（基于IP地址）
                    elif select == 5:
                        #删除httpd-vhosts.conf 1-100行内容
                        os.system("sed -i '1,100d' /etc/httpd/conf/extra/httpd-vhosts.conf")

                        b.based_on_ip_address()
                        continue
                    # 配置虚拟主机（基于端口）
                    elif select == 6:
                        # 删除httpd-vhosts.conf 1-100行内容
                        os.system("sed -i '1,100d' /etc/httpd/conf/extra/httpd-vhosts.conf")
                        # 删除httpd.conf 1-10000行内容
                        # os.system("sed -i '1,10000d' /etc/httpd/conf/httpd.conf")
                        b.based_on_port()
                        # 取消注释导入文件
                        os.system("sed -i '/httpd-vhosts/s/#//g' /etc/httpd/conf/httpd.conf")
                        continue
                    #返回主菜单
                    elif select == 10:
                        break


        #开启SELinux
        elif select == 20:
            start_SELinux()
        #关闭SELinux
        elif select == 21:
            stop_SELinux()

        elif select == 100:
            break
    except ValueError:
        print("您输入的字符类型不对，请重新输入！")


