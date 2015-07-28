# FastDFS概览
_整理：LeoTse_


## Definition
FastDFS是C语言实现的、开源的、轻量级的**应用级分布式文件系统**，开发者为淘宝开发平台部资深架构师余庆。它提供了负载均衡、冗余备份机制，是一个可扩展、高可用、高性能的分布式文件系统。

## Architecture
FastDFS一共由三部分组成：  
**TrackerServer**：负责负载均衡和调度。是整个FastDFS的中心，它将StorageServer的分组信息以及状态信息保存在内存中；  
**StorageServer**：存储文件和文件meta信息。直接使用操作系统的文件系统管理DFS上的文件；  
**Client**：使用者与请求发起方。通过专有接口，使用TCP/IP协议与跟踪器服务器或存储节点进行数据交互；  

![FastDFS架构](https://github.com/leotse90/blogs/blob/master/images/fdfs01.gif)

**上传文件**：  
![FastDFS上传文件](https://github.com/leotse90/blogs/blob/master/images/fdfs02.gif)

**下载文件**：  
![FastDFS下载文件](https://github.com/leotse90/blogs/blob/master/images/fdfs03.gif)

## Applies
适合大中型网站使用，用于视频、图片、音频等中小资源文件的存储。（建议范围：4KB<file_size<500MB）

## Features
### 1.Advantages
1）支持Linux、FreeBSD、AIX等Unix系统；  
2）支持Java、Python、PHP API；  
3）轻量级：相比GFS简化了master角色，不再管理meta数据信息；代码量较小，总代码行数不到5.2w行；  
4）对等结构：FastDFS集群中的TrackerServer也可以有多台，TrackerServer和StorageServer均**不存在单点问题**。TrackerServer之间是对等关系，组内的StoragServer之间也是对等关系。和MasterSlave结构相比，对等结构中所有结点的地位是相同的，每个结点都是Master，不存在单点问题；  
5）分组：FastDFS采用了分组存储方式。集群由一个或多个组构成，集群存储总容量为集群中所有组的存储容量之和。一个组由一台或多台存储服务器组成，同组内的多台StorageServer之间是互备关系，同组存储服务器上的文件是完全一致的。文件上传、下载、删除等操作可以在组内任意一台StorageServer上进行。所有的存储服务器均是同时在线服务，极大的提高的服务器的使用率，分担了数据访问压力；  
6）可以使用Apache、Nginx等WebServer访问和下载文件；  
7）FastDFS不对文件进行分块存储，与支持文件分块存储的DFS相比，更加简洁高效，并且完全能满足绝大多数互联网应用的实际需要。    
8）FastDFS的设计目标就是支持大容量和高访问量，因此对于大量的小文件，可以支持得很好；  

### 2.Disadvantages
1）FastDFS不支持POSIX接口方式，不是通用的文件系统，不支持FUSE，不能[mount使用](http://en.wikipedia.org/wiki/Mount_(Unix))；  
2）不适用于分布式计算环境；  
3）Group容量受单机存储容量限制，同时，当Group内有机器坏掉，数据恢复只能从Group内其他机器复制，使得恢复时间较长；  
4）FastDFS适合存储用户上传的文件，比如用户照片。如果只是存储网站的静态文件（如装饰图片、css、js等），那没有必要使用FastDFS；  
5）文档不够完善。相较于GlusterFS等DFS，FastDFS的相关文档资料相对欠缺。当前比较活跃的是ChinaUnix上的[FastDFS论坛](http://bbs.chinaunix.net/forum-240-1.html)。  


## others
来源于论坛原作者的话：  
1.单台tracker的性能特别高。因为tracker处理查询时，直接访问内存中的索引数据，不存在任何性能瓶颈。单台服务器支持的QPS超过5000没有任何问题。  

2.出于性能等考虑，必须通过FastDFS的API来对文件进行存取，不能mount使用。 

3.上传文件成功后，文件ID由storage server返回给客户端。文件ID中包括了分组、文件路径和文件名等信息，需要由客户端来保存文件ID。因此FastDFS 服务器端是不需要保存文件ID或索引等信息的。不再使用的文件（比如用户删除了自己的照片文件），应该由client调用delete file接口删除该文件。  

4.FastDFS存储文件采用的是256 * 256的两级目录；  

5.tracker不耗内存，有1GB内存足矣；   

6.FastDFS如何做整体迁移？如换机房更换IP?  

	如果新旧IP地址一一对应，而且是一样的，那非常简单，直接将data目录拷贝过去即可。

	IP不一样的话，会比较麻烦一些。
	如果使用了V4的自定义server ID特性，那么比较容易，直接将tracker上的IP和ID映射文件storage_ids.conf修改好即可。

	如果是用IP地址作为服务器标识，那么需要修改tracker和storage的data目录下的几个数据文件，将旧IP调整为新IP。
	注意storage的data目录下有一个.打头的隐藏文件也需要修改。
	另外，需要将后缀为mark的IP地址和端口命名的同步位置记录文件名改名。
	文件全部调整完成后才能启动集群服务。

	tracker server上需要调整的文件列表：
	data/storage_groups_new.dat
	data/storage_servers_new.dat
	data/storage_sync_timestamp.dat

	storage server需要调整的文件列表：
	data/.data_init_flag
	data/sync/${ip_addr}_${port}.mark：此类文件，需要将文件名中的IP地址调整过来。

7./etc/fdfs/mod_fastdfs.conf中的url_have_group_name项为true,否则会使用fdfs_test上传测试文件而后进行测试时，会报400错误。

8.[FastDFS监控系统](http://bbs.chinaunix.net/thread-3772130-1-4.html)

9.[FastDFS原理分析系列文章](http://bbs.chinaunix.net/thread-4164253-1-5.html)

10.部署方式和存储方式：作者推荐采用多个storage服务器(多个group)，各自分别挂载几个单盘的方式，以期提高总的磁盘IO性能。

11.相同内容的文件在系统里只保存一份文件实体，每次上传同一个文件，返回给client的文件ID是不同的，返回的文件ID通过链接的方式指向该实体文件，以unix的符号链接来理解：目标文件为实体文件，每次上传产生的文件为符号链接，指向对应的实体文件。

12.Storage的状态：  
    FDFS_STORAGE_STATUS：INIT      :初始化，尚未得到同步已有数据的源服务器  
    FDFS_STORAGE_STATUS：WAIT_SYNC :等待同步，已得到同步已有数据的源服务器  
    FDFS_STORAGE_STATUS：SYNCING   :同步中  
    FDFS_STORAGE_STATUS：DELETED   :已删除，该服务器从本组中摘除  
    FDFS_STORAGE_STATUS：OFFLINE   :离线  
    FDFS_STORAGE_STATUS：ONLINE    :在线，尚不能提供服务  
    FDFS_STORAGE_STATUS：ACTIVE    :在线，可以提供服务  

13.安装pcre时，出现  
configure: error: You need a C++ compiler for C++ support.  
解决方案：yum install -y gcc gcc-c++

14.上传文件时：  
errno: 113, error info: No route to host  
解决方案：有可能是防火墙问题。iptables -F

15.启动nginx，permission denied，这时一般是权限问题。  
解决方案：修改nginx配置，将#user  nobody;修改为user  root;（注意：可能有安全隐患），重启nginx即可。

## Conclusion
FastDFS，按照作者本人的说法，它把简洁和高效做到了极致，非常节约资源，中小网站完全用得起。  
作为国人在mogileFS的基础上进行改进的key-value型文件系统，一方面，它是我们国人的骄傲，另一方面，也希望FastDFS发展越来越好，相关的文档也越来越完善。

**备注**：  
该文档整理自网络，用于个人备忘与学习。如有侵权，衷心表示抱歉，并请联系本人及时删除相关内容。

**参考**：  
[分布式文件系统FastDFS原理介绍](http://tech.uc.cn/?p=221)  
[分布式文件系统FastDFS架构剖析](http://www.oschina.net/question/12_13316)  
[FastDFS 配置教程](http://blog.irebit.com/fastdfs-%E9%85%8D%E7%BD%AE%E6%95%99%E7%A8%8B/)  
[轻量级分布式文件系统FastDFS使用安装说明手册](http://blog.csdn.net/monkey_d_meng/article/details/6038995)  