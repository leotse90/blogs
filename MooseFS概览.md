# MooseFS概览

## Intro
[MooseFS](http://www.moosefs.org/)，是一种容错的网络分布式文件系统。它提供了FUSE接口的客户端，挂载后和读写本地磁盘上的文件无异，是替代NFS的理想选择。  
用户访问MooseFs系统中不同机器上的数据没有差异，对用户来说，只有一个源。

## Architecture
MooseFS主要由四部分组成：
### Master Server（元数据服务器）
管理整个MooseFS系统的单点，保存了MooseFS中每个文件的元数据，包括文件的大小、属性、文件位置等等；我们的元数据信息同时保存在Master的内存和磁盘里。
### Metalogger Server（元数据日志服务器）
存储元数据服务器的变更日志，用以恢复Master Server，它也会周期性下载MasterServer的元数据文件，服务器数量不定。我们也可以在Master Server宕掉后使用Metalogger Server作为我们的MasterServer；
### Chunk Server（数据存储服务器）
用于存储系统中的数据。如果我们指定数据需要备份（我们一般都会这么做），那么ChunkServer之间就会通过算法完成数据的备份工作；
### Client（客户端）
所有通过mfsmount进程和Master进行交互的机器，都可以叫做MooseFS的客户端。对客户端来说，所有的ChunkServer就像一台普通的NFS服务器一样在为它提供强大的数据存取服务；

笔者从MooseFS的官网上kiang了两张图，分别是MooseFS读数据和写数据的，大家闭上眼睛，用心感受下：  

![MooseFS Read Process](http://www.moosefs.org/tl_files/mfs_folder/read862.png)
![MooseFS Write Process](http://www.moosefs.org/tl_files/mfs_folder/write862.png)

我们从图上可以很清晰地看到整个读写过程。  

## Uses
1.大规模高并发的数据存储与访问（大文件、小文件皆可）；  
2.大规模的数据处理；

## Features
### Advantages
1）简单易用。安装、部署以及配置都相对简单容易；  
2）高可靠性：MooseFS采用数据备份的方式确保我们的数据安全可靠；  
3）可伸缩性：我们可以在不停服务的情况下，新增或者删除MooseFS中的服务器；  
4）支持POSIX访问，支持FUSE；  
5）可移植性：适用于任何实现FUSE的系统，包括但不限于Linux、FreeBSD、OpenSolaris以及MacOS X；  
6）MooseFS提供了快照功能，可以对整个文件甚至在正在写入的文件创建文件的快照；  
7）提供类似JVM的GC机制；  
8）提供web GUI监控接口；  
9）随机读写的效率较高，海量小文件读写效率高；  
10）发展比较成熟，文档全面；  

### Disadvantages
1）MooseFS客户端程序使用FUSE编写加载MooseFS磁盘的命令；因此我们需要确保我们系统内置或者安装了FUSE；  
2）存在单点故障。MooseFS只有一个Metadata Server，因此MDS的性能就会成为MooseFS性能的瓶颈；  
3）故障恢复需手动恢复;  
4）MooseFS的Master是单线程的程序，并不能发挥多核CPU的优势，由于大部分的处理逻辑都是内存操作，因此并不会存在太大的问题，但一旦涉及到磁盘I/O就有可能导致阻塞，严重的话整个集群会瘫痪掉，因此不建议把Master放在虚拟机中。[MooseFS之虚拟机惹的祸](http://tech.uc.cn/?tag=moosefs)

## Conclusion
当前，MooseFS在国际国内都拥有了大量的用户，正是由于这些用户基础，也推动了MooseFS继续发展。  
虽然MooseFS仍然存在单点故障这样的瓶颈，但是它的简单易用以及高可靠性，仍然让它成为我们DFS方案的不错的选择。

## Others
MooseFS官网解答了我们一些常见的问题：[FAQ](http://www.moosefs.org/moosefs-faq.html)

**NFS**：Network File System。一种用于分散式系统的协议。通过网络让不同的机器、不同的操作系统分享彼此个别的数据，让应用程序在客户端通过网络访问位于服务器磁盘中的数据，是在Unix系统间实现磁盘文件共享的一种方法。