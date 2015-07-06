# Python任务调度队列Celery
_BY:leotse_

## Introduction
在Python的使用过程中，我们常常会遇到执行一些多进程任务，或者一系列长时间的后台任务。比如，多进程下载视频并上传到某一个文件系统中。这时候，我们可以使用任务调度队列帮我们进行任务的分发与管理。

Celery就是这样一个任务队列，易于使用，入门简单。Celery常常需要第三方作为发送和接收消息的中间层，一般我们用到的有RabbitMQ、Redis、MongoDB等等，次等的选择也可以是数据库。

一般推荐使用RabbitMQ，但是我们这里用到Redis，因为Redis安装的时候依赖少，而且性能稳定，但是Redis也有缺点，那就是断电的时候会丢失数据。我们在这里，就以Redis作为Celery的第三方中间层。

## Installation
我们这里使用Celery+redis套餐进行任务的调度。  

Celery的安装非常简单，在linux系统下直接执行：  
`sudo pip install Celery`  
`sudo pip install celery-with-redis`  
如果上述安装失败，可以尝试：  
`sudo easy_install Celery`   

我们来验证一下Celery是否安装成功，进入python shell，输入：  
`from celery import Celery`  
如果没有报错，则说明安装成功。

接着我们安装redis：  
`sudo apt-get install redis-server`  
安装完成后，redis会自动启动，我们也来验证一下redis是否安装成功：  
`ps -aux|grep redis`  
如果看到以下输出，则说明安装ok：  
`redis      942  0.2  0.0  73852  1832 ?        Ssl  Apr13 302:26 /usr/bin/redis-server /etc/redis/redis.conf`

它们的安装都比较简单。接下来我们看如何使用Celery进行任务调度。

## Usage
我们应该都知道生产者-消费者模型，在使用Celery的时候，我们也需要一个生产者和一个消费者，生产者负责往队列里写入待处理的数据，消费者负责将数据从队列中取出并进行处理。我们在这里将redis作为存储这种“数据”的地方。

我们来看这样一个示例，我们假设要下载一批视频v1，v2，v3....，这批视频列表存在另一个文件系统中，我们假设通过get_video_list方法来获取这批视频列表，另一方面，我们可以通过download_video_worker(video)来下载视频。

那么，生产者的伪代码如下：
<pre><code>  
import download_video_worker
video_list = get_video_list()
for video in video_list: 
    download_video_worker.apply_async([video])
</pre></code>

消费者的伪代码如下： 
<pre><code> 
download_app=Celery("download_videos", broker="redis://localhost:6379/0")
@download_app.task`  
def download_video_worker(video):
    download_video_to_local(video)
</pre></code>

接着我们运行Celery：  
`celery -A download_video_worker worker --loglevel=info`  

这样，当我们每次往队列中放入video信息时，celery就会执行download_video_woker中的逻辑处理video的下载过程。


### 推荐阅读
[Homepage - Celery: Distributed Task Queue](http://www.celeryproject.org/)  
[CELERY - BEST PRACTICES](https://denibertovic.com/posts/celery-best-practices/)