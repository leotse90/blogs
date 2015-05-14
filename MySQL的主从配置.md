# MySQL的主从配置
整理：LeoTse

## 准备工作
我们假设有两台机器，操作系统为linux，其中一台作为Master，另一台作为Slave：  
Master：10.0.0.1  
Slave：10.0.0.2  
这两台机器都已经安装了MySQL数据库。  

## 主从配置
### Master配置
1.创建备份账户  
首先，我们在Master上专门为Slave访问Master进行数据备份建立一个账号，用户名为backup，密码为“backup_mysql”。我们在Master上执行以下SQL语句：  
`GRANT REPLICATION SLAVE, RELOAD, SUPER ON *.* TO backup@'10.0.0.2' IDENTIFIED BY 'backup_mysql';`  
如果我们有多个Slave，就执行上面的SQL多次，只需将backup@10.0.0.2中的IP改成其他Slave的IP。  
这个账号可以说是Slave访问Master的通行证。

2.Master配置  
如果Master的数据库已经有数据了，那么你需要先停下Master上的数据库并备份数据。

我们开始配置Master，修改/etc/mysql/my.cnf文件，找到[mysqld]段，增加以下字段：  
`log-bin         = mysql-bin`  
`server-id       = 1`  
`binlog-do-db    = test_db`  
`expire-logs-days= 7`  
下面来解释一下这些字段：  
`log-bin         = mysql-bin`表示启用二进制日志，用以记录Master中数据的更新日志；  
`server-id       = 1`唯一标识Master的ID，一般建议使用IP地址的最后一段；  
`binlog-do-db    = test_db`选择需要备份的数据库，**如果需要备份全部，可以不增加这行**；  
`expire-logs-days= 7`指定只保存7天的二进制日志，防止占用磁盘空间；  

配置好后，我们需要重启MySQL服务。  
`/etc/init.d/mysql restart`  

我们需要看看是否已经配置成功了，我们可以执行以下SQL语句：  
SHOW MASTER STATUS\G;  
如果你看到类似下面的信息，则说明Master基本ok：  
`            File: mysql-bin.000002`  
`        Position: 107`  
`    Binlog_Do_DB: test_db`  
`Binlog_Ignore_DB: `  


### Slave配置
Slave的配置也很简单。同样修改/etc/mysql/my.cnf文件，找到[mysqld]段，增加以下字段：  
`log-bin         = mysql-bin`  
`server-id       = 2`  
`binlog-do-db    = test_db`  
`relay-log       = mysql-relay-bin`  
`log-slave-updates = 1`  
我们解释一下2个在Master中没有出现的字段：  
`relay-log       = mysql-relay-bin`配置中继日志（主要是在MySQL服务器的主从架构中的Slave上用到的，当Slave想要和Master进行数据的同步时，从服务器将Master的二进制日志文件拷贝到自己的主机上放在中继日志中，然后调用SQL线程按照拷中继日志文件中的二进制日志文件执行以便就可达到数据的同步。）  
`log-slave-updates = 1`表示slave将复制事件写进自己的二进制日志；  

重启MySQL服务：  
`/etc/init.d/mysql restart`  

接下来就是让Slave连接Master，在Slave上执行以下SQL语句：  
`CHANGE MASTER TO MASTER_HOST='10.0.0.1',MASTER_USER='backup', MASTER_PASSWORD='backup_mysql', MASTER_LOG_FILE='mysql-bin.000001',MASTER_LOG_POS=0;`  
`START SLAVE\G;`  

最后，我们通过执行`SHOW SLAVE STATUS\G;`来查看是否配置成功，如果出现：  
`*************************** 1. row ***************************`  
`               Slave_IO_State: `  
`                  Master_Host: 10.0.0.1`  
`                  Master_User: backup`  
`                  Master_Port: 3306`  
`                Connect_Retry: 60`  
`              Master_Log_File: mysql-bin.000001`  
`          Read_Master_Log_Pos: 4`  
`               Relay_Log_File: mysqld-relay-bin.000001`  
`                Relay_Log_Pos: 4`  
`        Relay_Master_Log_File: mysql-bin.000001`  
`             Slave_IO_Running: No`  
`            Slave_SQL_Running: No`  
`              Replicate_Do_DB: `  
`          Replicate_Ignore_DB: `  
`           Replicate_Do_Table: `  
`       Replicate_Ignore_Table: `  
`      Replicate_Wild_Do_Table: `  
`  Replicate_Wild_Ignore_Table: `  
`                   Last_Errno: 0`  
`                   Last_Error: `  
`                 Skip_Counter: 0`  
`          Exec_Master_Log_Pos: 4`  
`              Relay_Log_Space: 107`  
`              Until_Condition: None`  
`               Until_Log_File: `  
`                Until_Log_Pos: 0`  
`           Master_SSL_Allowed: No`  
`           Master_SSL_CA_File: `  
`           Master_SSL_CA_Path: `  
`              Master_SSL_Cert: `  
`            Master_SSL_Cipher: `  
`               Master_SSL_Key: `  
`       Seconds_Behind_Master: NULL`  
`Master_SSL_Verify_Server_Cert: No`  
`                Last_IO_Errno: 0`  
`                Last_IO_Error: `  
`               Last_SQL_Errno: 0`  
`               Last_SQL_Error: `  
`  Replicate_Ignore_Server_Ids: `  
`             Master_Server_Id: 0`  

那么恭喜你，配置成功。

至此，整个MySQL主从集群已经搭建好了。