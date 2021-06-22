# -*- coding:UTF-8 -*-
# 作者：张子涵
# 开始时间：2021/6/20
# 结束时间：2021/6/20
import os

def local_yum():
    #挂载光盘
    os.system("mount /dev/cdrom /mnt")

    #备份源
    if not os.path.exists("/backup"):
        os.mkdir("/backup")
        os.system("mv /etc/yum.repos.d/* /backup")
    else:
        os.system("mv /etc/yum.repos.d/* /backup")

    #删除源文件
    os.system("rm -rf /etc/yum.repos.d/*")

    #编辑yum源文件

    if not os.path.exists("/etc/yum.repos.d/local.repo"):
        with open("/etc/yum.repos.d/local.repo", 'w',encoding="utf-8") as f:
            f.write('''[local-media]
name=CentOS-$releasever - Media
baseurl=file:///mnt
gpgcheck=0
enabled=1''')
    else:
        with open("/etc/yum.repos.d/local.repo", 'w',encoding="utf-8") as f:
            f.write('''[local-media]
name=CentOS-$releasever - Media
baseurl=file:///mnt
gpgcheck=0
enabled=1''')

    #清空yum缓存目录
    os.system("yum clean all")

    #生成yum元数据
    os.system("yum makecache")

if __name__ == '__main__':
    local_yum()
