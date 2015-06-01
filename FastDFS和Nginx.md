# FastDFS和Nginx
by：Leo Tse

## Intro
FastDFS，国产分布式文件系统，轻便而快捷，简单又灵活，兼顾了高可用、可扩展及高性能，它在国内不少公司得到部署使用。（参见[FastDFS概览](https://github.com/leotse90/blogs/blob/master/FastDFS%E6%A6%82%E8%A7%88.md)）。但是，FastDFS自身并不提供http服务（注：以前的老版本是提供HTTP服务的，但是由于性能不佳，原作者不建议使用），因此我们需要依靠其他的WebService来提供Storage的HTTP访问服务。一般地，我们选择Nginx或者Apache作为我们的WebService提供者。  
我们在这里主要介绍FastDFS与Nginx配合提供HTTP访问。

## FastDFS+Nginx
首先，你得有一个FastDFS集群，然后，你得部署好Nginx（FastDFS+Nginx集群部署请看[FastDFS安装使用说明](https://github.com/leotse90/blogs/blob/master/FastDFS%20%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.md)）。

一般情况下，Nginx只对外提供当前Storage的文件访问HTTP服务。因此，我们必须在每台Storage服务器上都部署Nginx以及ngx-http-fastdfs-module。我们可以在mod_fastdfs.conf配置文件中配置FastDFS nginx模块的一些主要参数。比如response_mode字段，这个我们用以指定Nginx的响应模式。

**Nginx在这里充当什么角色？**   
一般情况下，在FastDFS文件系统中，Nginx的角色是单一的HTTP访问服务，这也是Nginx最基本的功能。有些用户可能会觉得Nginx在这里有点大材小用，其实，本人也是这样认为的，并且期待FastDFS作者能在FastDFS中集成可靠的HTTP服务。  
当然也有人说，FastDFS作为分布式文件系统，它的职责就是进行文件存储，使得文件的存储可靠而高效，它完全没有义务提供额外的HTTP服务。这就完全是仁者见仁了。

**上文提到的Nginx响应模式，能否大概介绍下？**  
我们首先简单说一下FastDFS的文件同步方式，它是主从式同步，也就是它有一个源Storage，Storage服务器下载完文件后就告诉客户端已经ok了，然后由源Storage负责将文件同步到其他的Storage。  
在HTTP访问FastDFS上的文件时，如果由于同步延迟问题造成最新的文件A并没有同步到所有的Storage上，这时，如果用户访问还没来得及同步A文件的Storage，就会Not Found，Nginx模块这时就可以帮我们解决同步延时问题。  
我们在mod_fastdfs.cong中可以看到response_mode响应模式有两种：redirect和proxy。如果当前的Storage找不到文件A，根据我们配置，会出现以下两种情况之一：  
1）proxy：代理模式。工作原理如同反向代理的做法，而仅仅使用源storage地址作为代理proxy的host，其余部分保持不变；  
2）redirect：重定向。该模式下要求源Storage配备公开访问的webserver、同样的端口、同样的path配置。因为是同意配置，这点我们一般能满足。此时服务端返回302响应码，url如下：
`http:// {源storage地址} : {当前port} {当前url} {参数"redirect=1"}(标记已重定向过)`

**当某台Storage上的Nginx模块挂了，Tracker能否感知并中断其提供HTTP访问？**  
很遗憾，不能！！   
是不是很抓狂！毕竟FastDFS和Nginx作为两个独立的产品。不过，不要沮丧，我们可以做统一的访问代理来解决，Storage 的nginx上再加一层nginx做反向代理。退一步，我们可以自己增加对Nginx服务的监控。


### 参考：
[FastDFS使用经验分享](http://tech.uc.cn/?p=2579)  
[fastdfs-nginx扩展模块源码分析](http://www.cnblogs.com/littleatp/p/4361318.html)