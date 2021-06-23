# -*- coding:UTF-8 -*-
# 作者：张子涵

import os
from config_local_yum import local_yum
from DHCP import *
from FTP import *

def start_service(service):
    os.system("sudo systemctl start %s"%service)
    return start_service


def stop_service(service):
    os.system("sudo systemctl stop %s"%service)
    return stop_service

def restart_service(service):
    os.system("sudo systemctl restart %s"%service)
    return restart_service

def status_service(service):
    os.system("sudo systemctl status %s"%service)
    return status_service

def start_SELinux():
    os.system("sudo setenforce 1")
    print("您已开启SELinux!")

def stop_SELinux():
    os.system("sudo setenforce 0")
    print("您已关闭SELinux!")

def show_services(select):
	if select == 3:
		os.system("sudo systemctl list-unit-files | grep enabled | awk '{print $1}'")
		return show_services
	elif select == 4:
		os.system("sudo systemctl list-unit-files | grep disabled | awk '{print $1}'")
		return show_services


while True:
    print("(0)查看服务状态\n(1)开启服务\n(2)关闭服务\n(3)重启服务\n(4)查看开启的服务\n(5)查看关闭的服务\n(6)安装服务或软件\n(7)卸载服务或软件\n(8)配置本地yum源\n(9)配置DHCP\n(10)配置FTP\n(20)开启SELinux\n(21)关闭SELinux\n(100)退出\n")
    try:
        select = int(input("请选择服务选项:"))
        # 查看服务状态
        if select == 0:
            service = input("请输入服务名称:")
            status_service(service)
        elif select == 1:
            service = input("请输入服务名称:")
            start_service(service)
            print("您已开启服务！")
        elif select == 2:
            service = input("请输入服务名称:")
            stop_service(service)
            print("您已关闭服务！")
        elif select == 3:
            service = input("请输入服务名称:")
            restart_service(service)
            print("您已重启服务！")
        elif select == 4:
            show_services(select)
        elif select == 5:
            show_services(select)
        elif select == 6:
            service = input("请输入服务名称:")
            os.system("yum install %s -y" % service)
        elif select == 7:
            service = input("请输入服务名称:")
            os.system("yum remove %s -y" % service)
        #配置本地yum源
        elif select == 8:
            local_yum()
        #配置DHCP
        elif select == 9:
            a = Configure_DHCP()
            if a.backup() == "系统未检测到dhcpd服务，请安装！":
                print(a.backup())
                continue
            else:
                a.backup()
                a.build_main_file()

        #配置FTP
        elif select == 10:
            a = Configure_FTP()
            if a.backup() == "系统未检测到vsftpd服务，请安装！":
                print(a.backup())
                continue
            else:
                a.backup()
                a.select_mode()

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

