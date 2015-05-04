# FastDFS概览
_整理：LeoTse_


## Definition
FastDFS是C语言实现的、开源的、轻量级的**应用级分布式文件系统**，开发者为淘宝开发平台部资深架构师余庆。它提供了负载均衡、冗余备份机制，是一个可扩展、高可用、高性能的分布式文件系统。

## Architecture
FastDFS一共由三部分组成：  
**TrackerServer**：负责负载均衡和调度。是整个FastDFS的中心，它将StorageServer的分组信息以及状态信息保存在内存中；  
**StorageServer**：存储文件和文件meta信息。直接使用操作系统的文件系统管理DFS上的文件；  
**Client**：使用者与请求发起方。通过专有接口，使用TCP/IP协议与跟踪器服务器或存储节点进行数据交互；  

![FastDFS架构](http://www.programmer.com.cn/wp-content/uploads/2010/11/%E5%88%86%E5%B8%83%E5%BC%8F%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9FFastDFS%E6%9E%B6%E6%9E%84%E5%89%96.gif)

**上传文件**：  
![FastDFS上传文件](http://www.programmer.com.cn/wp-content/uploads/2010/11/%E5%88%86%E5%B8%83%E5%BC%8F%E6%96%87%E4%BB%B62.gif)

**下载文件**：  
![FastDFS下载文件](http://www.programmer.com.cn/wp-content/uploads/2010/11/%E5%88%86%E5%B8%83%E5%BC%8F%E6%96%87%E4%BB%B63.gif)

## Uses
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
4）FastDFS适合存储用户上传的文件，比如用户照片。如果只是存储网站的静态文件（如装饰图片、css、js等），那没有必要使用FastDFS。  

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