# Linux上Python版本升级
__整理：leotse__

### 目标  
将linux上的python版本升级到较高的版本。

### 环境
我们假定服务器操作系统为RedHat（不同OS大同小异），python版本由2.6升级到2.7。在升级前，你需要确定是否会影响当前的工程和项目的运行。

### 升级
1.下载python2.7安装包：  
`wget http://python.org/ftp/python/2.7.2/Python-2.7.2.tgz`

2.安装python2.7:  
`tar -zxvf Python-2.7.2.tgz`  
`cd Python-2.7.2`  
`./configure --prefix=/usr/local/python27`  
`make`  
`sudo make install`  

3.覆盖原来的python：  
`sudo mv /usr/bin/python /usr/bin/python_old`  
`sudo ln -s /usr/local/python27/bin/python /usr/bin/`

4.验证Python安装，输入`python`，查看版本。

### 其他
升级python版本的一个后遗症就是yum无法正常工作，只需要做一点点修改即可：  
`sudo /usr/bin/yum`  
将第一行  
`#!/usr/bin/python`  
改成原来的版本，在这里我们改成：  
`#!/usr/bin/python2.6`  

再次输入yum即可发现已经ok了！