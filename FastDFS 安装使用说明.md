# FastDFS安装使用说明
整理：LeoTse

## 一、概述
FastDFS是C语言实现的、开源的、轻量级的应用级分布式文件系统，开发者为淘宝开发平台部资深架构师余庆。它提供了负载均衡、冗余备份机制，是一个可扩展、高可用、高性能的分布式文件系统。  
更多内容见论坛：[http://bbs.chinaunix.net/forum-240-1.html](http://bbs.chinaunix.net/forum-240-1.html)

本文档内容包括：FastDFS安装、Python API安装及调用、通过Nginx访问文件。FastDFS安装又包括Tracker、Storage以及Nginx的安装。  

## 二、准备工作
1.建议先了解一下FastDFS；  

2.所用到的环境或软件有如下一些：  
1）Ubuntu 12.04  
2）libfastcommon-master.zip  
3）fastdfs-5.05.tar.gz  
4）fastdfs-nginx-module_v1.16.tar.gz  
5）nginx-1.9.0.tar.gz  
6）pcre-8.33.tar.gz  
7）zlib-1.2.8.tar.gz  
8）fdfs_client-py-master.zip  
虽然看起来用到的软件比较多，但是安装配置过程比较简单。（注：相关软件都可以在本压缩文件中找到。）  

3.我们假设我们用到的机器有：  
**Tracker**：192.168.9.229  
**Storage**：192.168.9.230， 192.168.9.231  

## 三、安装步骤
### 1.安装libfastcommon（Tracker和Storage都需要）：  
相较于旧版的FastDFS，新版的FastDFS已经不需要依赖libevent，我们需要先安装它的依赖包libfastcommon。  
a)解压libfastcommon-master.zip：  
unzip libfastcommon-master.zip  

b)进入libfastcommon-master目录，执行：  
./make.sh  
./make.sh install   

我们可以看到libfastcommon.so安装到了/usr/lib64/libfastcommon.  so。但是FastDFS主程序设置的目录lib的目录是/usr/local/lib，所以需要创建软连接：  
ln -s /usr/lib64/libfastcommon.so /usr/local/lib/libfastcommon.so  
ln -s /usr/lib64/libfastcommon.so /usr/lib/libfastcommon.so  
ln -s /usr/lib64/libfdfsclient.so /usr/local/lib/libfdfsclient.so  
ln -s /usr/lib64/libfdfsclient.so /usr/lib/libfdfsclient.so   

### 2.安装FastDFS（Tracker和Storage都需要）：  
a）解压fastdfs-5.05.tar.gz；  
tar -xzvf fastdfs-5.05.tar.gz  
b）进入fastdfs-5.05目录，依次执行：  
cd fastdfs-5.05  
./make.sh  
./make.sh install  
到此我们的安装暂时结束，相应的配置等会会介绍到。我们下一步来安装Nginx依赖。

### 3.安装Nginx依赖模块（只需要在Storage上安装，如果需要Tracker直接提供文件访问服务，Tracker也需安装）：  
FastDFS通过HTTP服务器来去提供HTTP服务。我们采用Nginx作为HTTP服务器，因为Nginx能支持高并发的访问并提供负载均衡等高性能的服务。  
我们约定，所有的这些包都在/home/leotse/fastdfs/下。  
a）fastdfs-nginx-module安装:  
我们知道FastDFS通过Tracker将用户上传的文件保存在Storage服务器上，但是同一个Group上的机器进行文件复制会有一定的延时。假设我们有A、B两台Storage服务器，一开始c文件保存在A，在c文件复制到B服务器之前用户到B服务器访问c文件，势必会报错，fastdfs-nginx-module的作用就是重定向到源服务器（即示例中的A）读文件，避免了复制延迟的问题。  
tar -xzvf fastdfs-nginx-module_v1.16.tar.gz  
我们需要根据fastdfs以及fastcommon的文件位置判断是不是需要修改config文件。  
CORE_INCS="$CORE_INCS /usr/local/include/fastdfs /usr/local/include/fastcommon/"  
改成：  
CORE_INCS="$CORE_INCS /usr/include/fastdfs /usr/include/fastcommon/"  

b）zlib库安装：  
tar -xzvf zlib-1.2.8.tar.gz  
cd zlib-1.2.8  
设置安装路径并安装：  
./configure --prefix=/usr/local/zlib  
make  
make install  

c）pcre库安装：  
tar -xzvf pcre-8.33.tar.gz  
cd pcre-8.33  
./configure --prefix=/usr/local/pcre --libdir=/usr/local/lib/pcre --includedir=/usr/local/include/pcre  
make  
make install  

### 4.安装Nginx：  
a）解压Nginx安装包：  
tar -xzvf nginx-1.9.0.tar.gz  

b）进入Nginx目录并设置安装路径以及指定依赖库：  
cd nginx-1.9.0  
./configure --prefix=/usr/local/nginx \  
--with-zlib=/home/leotse/fastdfs/zlib-1.2.8\  
--with-pcre=/home/leotse/fastdfs/pcre-8.33\  
--sbin-path=/usr/local/nginx\  
--add-module=/home/leotse/fastdfs/fastdfs-nginx-module/src  

c）make安装：  
make  
make install  

### 5.Tracker配置与启动：  
在配置之前，非常郑重地推荐这个：[FastDFS 配置文件详解(修订版1) ](http://bbs.chinaunix.net/thread-1941456-1-1.html)，里面非常详尽地介绍了FastDFS的配置文件具体参数。  

a）修改tracker.conf文件，该文件的位置在fastdfs-5.05/conf下。在此之前，我们需要创建一个目录存放Tracker的data和log，我们在这里假定这个路径为：/home/leotse/fastdfs/tracker/，我们需要确保该路径存在。我们只需要修改：  
base_path=/home/leotse/fastdfs/tracker/  

b）复制tracker.conf文件到/etc/fdfs/目录下：  
cp tracker.conf /etc/fdfs/  

c）运行Tracker：  
fdfs_tracker /etc/fdfs/tracker.conf   
停止Tracker：/usr/local/bin/stop.sh fdfs_tracker /etc/fdfs/tracker.conf   
重启Tracker：/usr/local/bin/restart.sh fdfs_tracker /etc/fdfs/tracker.conf 

### 6.Storage配置与运行：  
在这里，同样我们需要创建一个目录保存Storage的data和log，我们假定Storage上该目录为/home/leotse/fastdfs/storage/。  
a）修改Nginx端口（可选）：  
Nginx默认的端口号为80，为了防止引起冲突，我们建议修改Nginx的端口：  
vi /usr/local/nginx/conf/nginx.conf  
修改  
    server {  
        listen       80;  
        server_name  localhost;  
在这个示例里，我们将80改为9096（可以更改）。  

b）在Nginx中支持FastDFS模块：  
vi /usr/local/nginx/conf/nginx.conf  
我们在server模块中增加：  
location /group1/M00{  
    root /home/leotse/fastdfs/storage/data;  
    ngx_fastdfs_module;  
}    

c）给Storage的存储目录做一个软连接：  
 ln -s /home/leotse/ fastdfs /storage/data  /home/leotse/ fastdfs /storage /data /M00  

d）修改Storage配置。我们将注意力从Nginx转到FastDFS上来，  
修改storage.conf文件，该文件的位置在fastdfs-5.  05/conf下，我们需要创建目录/home/leotse/fastdfs/storage/用以保存Storage的data和logs。我们需要做以下修改：  
修改group_name，根据实际配置确定：  
group_name=group1  
接下来修改存储data和logs的目录：  
base_path=/home/leotse/fastdfs/storage/  
然后就是放置文件的目录，需要和nginx中的server中的设置保持一样。建议与上面的目录保持一致：  
store_path0=/home/leotse/fastdfs/storage/  
接着就是修改Tracker的host，如果有多个Tracker可以分行写：  
tracker_server=192.169.9.229:22122  
然后就是配置web server的端口，需要和Nginx的端口保持一致：  
http.server_port=9096  
修改storage.conf文件后，将其copy到/etc/fdfs/目录下：  
cp storage.conf /etc/fdfs/  

e）修改fastdfs-nginx-module配置：  
将mod_fastdfs.conf复制到/etc/fdfs/目录下：  
cp mod_fastdfs.conf /etc/fdfs/  
修改mod_fastdfs.conf文件：  
vi /etc/fdfs/mod_fastdfs.conf  
修改base_path以及store_path0，使其和storage.conf中保持一致：  
base_path=/home/leotse/fastdfs/storage/  
store_path0=/ home/leotse/fastdfs/storage/    
修改tracker server以及group_name：  
tracker_server=192.168.9.229:22122  
group_name=group1  
修改group count，注意，如果只有单个group，设置为0，如果有多个group，根据实际情况配置：  
group_count = 0  
在url中包含group name，一定要设置为true：  
url_have_group_name = true  
修改完毕。  

conf目录下的http.conf和mime.types两个文件也需要copy到/etc/fdfs目录下。

运行nginx：  
/usr/local/nginx/sbin/nginx  
运行Storage：  
fdfs_storaged /etc/fdfs/storage.conf  
停止Storage：  
/usr/local/bin/stop.sh fdfs_storaged /etc/fdfs/storage.conf  
重启Storage：  
/usr/local/bin/restart.sh fdfs_storaged /etc/fdfs/storage.conf

### 7.运行：  
我们已经成功配置了Tracker和Storage以及Nginx，接下来就是上传和下载文件。  
我们这里要用到client.conf文件来获取FastDFS的相关信息，该文件在fastdfs中的conf目录下：  
修改如下地方：  
base_path=/home/leotse/fastdfs/tracker  
tracker_server=192.168.9.229:22122  
http.tracker_server_port=9096    

我们可以直接使用直接调用或者调用API（我们这里介绍的是Python API）。  
首先是直接调用，我们假设/home/leotse/test/下有文件test_fdfs.txt  
fdfs_test /etc/fdfs/client.conf upload /home/leotse/test/test_fdfs.txt  
我们可以看到这样的返回：  
example file url: http://192.168.9.230:9096/group1/M00/00/08/wKgJ5lVPFzCAJVXwAAApRhJa9hc052_big.txt  
我们可以通过这个url获取这个文件。  

接下来介绍Python API调用。我们首先要获取最新的python api包，我们这里用到的是fdfs_client-py-master.  zip。我们将其在机器上解压，然后调用：  
python setup.py install  
安装完毕后即可调用。
我们主要用到的方法有：  
上传文件：upload_by_filename  
下载文件：download_to_file  
删除文件：delete_file  
我们在这里也上传了两个脚本（与该blog在同一级目录），fdfs_test.py演示了Python API的使用方法，fdfs_nginx_test.py演示了如何以nginx的方式下载文件。  

## 四、FastDFS性能测试  
我们测试了FastDFS的性能，主要是Python API的上传文件以及下载文件， Nginx下的下载文件性能，下面为测试结果：  

a）FastDFS Python API Test Results:  
==============================result============================  
file size: 8.00MB  
upload files 20 times  
failed upload 0 times  
rate of failed upload: 0.0 %    
upload average duration: 0.317473113537 s  
download average duration: 0.165269041061 s  

==============================result============================  
file size: 39.00MB  
upload files 20 times  
failed upload 0 times  
rate of failed upload: 0.0 %  
upload average duration: 1.21865663528 s  
download average duration: 0.707462477684 s  

==============================result============================  
file size: 128.00MB  
upload files 20 times  
failed upload 0 times  
rate of failed upload: 0.0 %  
upload average duration: 3.0637313962 s  
download average duration: 1.59568111897 s  

=============================result=============================  
file size: 336.00MB  
upload files 20 times  
failed upload 0 times  
rate of failed upload: 0.0 %  
upload average duration: 5.62887555361 s  
download average duration: 4.49918934107 s  

b）FastDFS Nginx Download Test Results:  
==============================result============================  
file size: 8.00MB  
download file 50 times  
failed 0 times  
rate of failed download: 0.0 %  
average download duration: 0.0893847703934 s  

==============================result============================  
file size: 39.00MB  
download file 50 times  
failed 0 times  
rate of failed download: 0.0 %  
average download duration: 0.36199669838 s  

==============================result============================  
file size: 128.00MB  
download file 50 times  
failed 0 times   
rate of failed download: 0.0 %  
average download duration: 1.27810112 s  

==============================result============================  
file size: 336.00MB  
download file 50 times  
failed 0 times  
rate of failed download: 0.0 %  
average download duration: 3.0081551671 s  
