# Hadoop集群部署（RedHat）
__整理：LeoTse__

## 概述
安装环境：Red Hat 4.8.3-9  
Hadoop版本：Apache Hadoop 2.6.0  
Java版本：1.8.0  
Master：172.16.10.136  
Slave1：172.16.10.137  
用户：xiefeng  
安装目录：/home/xiefeng/dependencies

主要部署步骤：  
1.SSH免密码登录设置；  
2.环境变量设置（Java以及Hadoop）;  
3.Master部署；  
4.Slave部署；  
5.启动集群；  

接下来我们对每一步进行详细介绍。

## SSH免密码登录设置
进行SSH免密码登录设置是为了避免在集群内部机器交互的时候频繁输入登录密码，我们在这里为集群内的每个机器都执行SSH免密码登录设置。在这里不具体介绍SSH免密码登录的具体步骤，可以参见[SSH免密码登录设置](https://github.com/leotse90/blogs/blob/master/SSH免密码登录设置.md)

## 环境变量设置
修改hosts文件：  
`vi /etc/hosts`  
新增：  
`172.16.10.136   Master`  
`172.16.10.137   Slave1`  

一般，Java都已经安装好。如果没有，需要先行安装Java并配置JAVA_HOME。然后修改~/.bashrc文件，在文件的末尾增加JAVA和HADOOP的配置：  

`### set java home`  
`export JAVA_HOME=/work/p/jdk/default`  

`### set hadoop env`  
`export HADOOP_HOME=/home/xiefeng/dependecies/hadoop-2.6.0`  
`export HADOOP_COMMON_HOME=$HADOOP_HOME`  
`export HADOOP_HDFS_HOME=$HADOOP_HOME`  
`export HADOOP_MAPRED_HOME=$HADOOP_HOME`  
`export HADOOP_YARN_HOME=$HADOOP_HOME`  
`export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop`  
`export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HADOOP_HOME/lib`  
`export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native`  
`export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib"`  

然后：  
`source ~/.bashrc`  

检查是否配置成功，可以`echo $HADOOP_HOME`看是否是配置中的路径。  

## Master部署
1.解压Hadoop 2.6安装包到安装目录，在这个示例里是/home/xiefeng/dependecies/目录：  
`tar xvf hadoop-2.6.0.tar`  

2.进入Hadoop目录，修改slaves文件，增加Slave1到slaves文件中：  
`cd hadoop-2.6.0`  
`vi etc/hadoop/slaves`  
添加：  
`Slave1`  

3.修改core-site.xml配置文件：  
`vi etc/hadoop/core-site.xml`  
修改为：  
<configuration>  
<property>  
    <name>fs.defaultFS</name>  
    <value>hdfs://Master:9000</value>  
</property>  
<property>  
    <name>hadoop.tmp.dir</name>  
    <value>file:/home/xiefeng/dependecies/hadoop-2.6.0/tmp</value>  
    <description>Abase for other temporary directories.</description>  
</property>  
</configuration>  

4.修改hdfs-site.xml配置文件为：  
<configuration>  
<property>  
    <name>dfs.namenode.secondary.http-address</name>  
    <value>Master:50090</value>  
</property>  
<property>  
    <name>dfs.namenode.name.dir</name>  
    <value>file:/home/xiefeng/dependecies/hadoop-2.6.0/tmp/dfs/name</value>  
</property>  
<property>  
    <name>dfs.datanode.data.dir</name>   
    <value>file:/home/xiefeng/dependecies/hadoop-2.6.0/tmp/dfs/data</value>  
</property>  
<property>   
    <name>dfs.replication</name>   
    <value>1</value>  
</property>  
</configuration>  

5.复制mapred-site.xml.template得到mapred-site.xml文件：
`cp mapred-site.xml.template mapred-site.xml`  
修改mapred-site.xml配置文件为：  
<configuration>  
<property>  
    <name>mapreduce.framework.name</name>  
    <value>yarn</value>  
</property>  
</configuration>  

6.修改yarn-site.xml配置文件为：  
<configuration>  
<!-- Site specific YARN configuration properties -->  
<property>  
    <name>yarn.resourcemanager.hostname</name>  
    <value>Master</value>  
</property>  
<property>  
    <name>yarn.nodemanager.aux-services</name>  
    <value>mapreduce_shuffle</value>  
</property>  
</configuration>  

## Slave部署
1.将 Master 上的 Hadoop 文件先打包然后复制到各个节点上：  
`sudo tar -zcf hadoop－2.6.0.tar.gz hadoop－2.6.0/`  
`scp hadoop－2.6.0.tar.gz Slave1:/home/xiefeng/dependecies`  

2.解压到Slave1的安装目录：  
`sudo tar -zxf hadoop－2.6.0.tar.gz`   
`sudo chown -R xiefeng:xiefeng /home/xiefeng/dependecies/hadoop-2.6.0`  

## 集群启动
我们回到Master，进入hadoop安装目录：  
`cd /home/xiefeng/dependecies/hadoop-2.6.0`  
第一次执行，初始化：  
`bin/hdfs namenode -format`  

启动dfs：  
`sbin/start-dfs.sh`  
启动yarn：  
`sbin/start-yarn.sh`  

分别在Master和Slave1输入jps，看看是否有以下输出，有则表明安装ok：  
`[xiefeng@Master hadoop-2.6.0]$ jps`  
`8498 NameNode`  
`8837 ResourceManager`  
`8680 SecondaryNameNode`  
`9817 Jps`  

`[xiefeng@Slave1 logs]$ jps`  
`20208 NodeManager`  
`20344 Jps`  
`20107 DataNode`  

在浏览器输入：http://master：8088就可以查看集群All Applications信息；输入http://master:50070可以查看namenode信息。


停止dfs：  
`sbin/stop-dfs.sh`  
停止yarn：  
`sbin/stop-yarn.sh`  


另外，还可以使用以下脚本进行集群的启动和停止：  
`sbin/start-all.sh`  
`sbin/stop-all.sh`

至此，Hadoop集群搭建完毕！！！