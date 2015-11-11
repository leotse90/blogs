# ElasticSearch与MySQL数据同步以及修改表结构
_by:leotse_

## ES与MySQL的数据同步
如果你需要进行ES与MySQL的数据同步，亦即将MySQL中的数据导入到ES中，并保持同步，一般来看，有以下几种方法：  
1.自己动手写一个同步的模块。实时tail处理MySQL的binlog，将数据库的新增、修改或删除这些操作同步在ES上执行。这种方案可行，但是实现起来代价大；

2.[go-mysql-elasticsearch](https://github.com/siddontang/go-mysql-elasticsearch)。这是Git上的一个开源项目，差不多是第一种方案的一个实现版本。这个插件支持实时同步MySQL与ES的新增、修改以及删除操作。但是缺点是使用起来不够灵活，它的作者给出了它的以下缺点：
>binlog row image must be full for MySQL, you may lost some field data if you update PK data in MySQL with minimal or noblob binlog row image. MariaDB only supports full row image.  
>Can not alter table format at runtime.   
>mysqldump must exist in the same node with go-mysql-elasticsearch, if not, go-mysql-elasticsearch will try to sync binlog only.

这三点比较重要的缺点影响我使用这种方案，特别是不能运行时修改表结构。对于很多在线业务来说是比较难以接受的。

3.[elasticsearch-river-jdbc](https://github.com/jprante/elasticsearch-jdbc)。这种方案是1、2的结合体。可以较为灵活地进行数据同步，比如可以在同步的时候指定需要同步的字段以及筛选条件。这也是比较流行的解决方案，但是它也有一个比较致命的缺点，那就是删除操作不能同步（物理删除）！

如果你的系统对删除操作频繁，而且都是物理删除，并且能接受不能运行时修改表结构等条件，那么使用go-mysql-elasticsearch将是非常不错的选择；如果你的表结构改变得相对频繁，而且不用对表进行物理删除（比如用逻辑删除取而代之），那么你可以选择elasticsearch-river-jdbc。如果你对这两者都不满意，而且觉得自己的编码能力还不错，那么完全可以自己定制一个满足自己需求的插件。

## elasticsearch-river-jdbc使用
我们这里选择使用elasticsearch-river-jdbc作为我们同步ES与MySQL的插件。我们这里简单介绍一下elasticsearch-river-jdbc的安装与使用：
1.确保ES的集群的每个Node都能访问MySQL数据库；  

2.安装River：  
```
>./bin/plugin --install river-jdbc --url  http://xbib.org/repository/org/xbib/elasticsearch/plugin/elasticsearch-river-jdbc/1.5.0.5/elasticsearch-river-jdbc-1.5.0.5-plugin.zip
```
3.下载mysql-connector-java-5.1.30-bin.jar并将其保存在{$ES_HOME}/plugins/jdbc/目录下：
```
wget http://cdn.mysql.com//Downloads/Connector-J/mysql-connector-java-5.1.37.tar.gz
```
如果是ES集群，你需要在每一个Node上执行这一步。

4.创建一个JDBC river
```
>curl -XPUT 'localhost:9200/_river/my_jdbc_river/_meta' -d '{
     "type" : "jdbc”,
     "jdbc" : {
         "driver" : "com.mysql.jdbc.Driver",
         "url" : "jdbc:mysql://localhost:3306/test",
         "user" : “root",
         "password" : “123456",
         "sql" : "select * from test.student;”,
         "interval" : "30",
         "index" : "test",
         "type" : "student"
     }
 }’
 ```

 5.你可以查看ES是否已经同步了这些数据：
 ```
 > curl -XGET 'localhost:9200/test/student/_search?pretty&q=*'
 ```

## 修改表结构后的数据同步
如果你需要修改正在与ES进行数据同步的表的结构，你有以下三种方案（亲测可行）：    
**方案一**：创建JDBC river的时候使用sql语句：`select * from table_name;`
乍一看，这种方法很坑。但是确实适合那些喜欢简单粗暴的coder。但是这种方案的场景比较苛刻：   
>MySQL中表在创建时id命名为_id，这是因为_id是ES中每一条document的唯一标识；如果不这样干，你会发现每一次同步ES的type中都会增加MySQL表中条目数个Document；    
>MySQL表所有的字段对ES都是有效的、必要的；

**方案二**.方案一的改进版，使用sql语句：`select *, id as _id from table_name;`  
这个方案在你需要在ES中存储MySQL中表所有字段的时候变得比较有效。

**方案三**：使用elasticsearch的alias。具体的操作比较简单，可以参照[官网的介绍](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html)。

前两种方案有点取巧，第三种方案才是正道。


如果你愿意，完全建议自己定制一套解决方案。由于业务需要，本人最近也在开始写这样的插件。我会在这个博客里保持更新。