# ElasticSearch初探
_by:leotse_

## ES介绍
我们首先来看[ES](https://www.elastic.co)（全称是Elastic Search）到底是什么，下面是Wikipedia给出的定义：
>Elasticsearch is a search server based on Lucene. It provides a distributed, multitenant-capable full-text search engine with a RESTful web interface and schema-free JSON documents. Elasticsearch is developed in Java and is released as open source under the terms of the Apache License. Elasticsearch is the second most popular enterprise search engine after Apache Solr.

>ElasticSearch是一个基于Lucene的搜索服务器。它提供了一个分布式多用户能力的全文搜索引擎，基于RESTful web接口。Elasticsearch是用Java开发的，并作为Apache许可条款下的开放源码发布，是第二流行的企业搜索引擎。

在这段定义之外，我们看看ES还有哪些吸引人的地方：  
1.ES的搜索几乎是实时的，当你向一个ES服务器或者一个ES集群发出搜索请求后，你可以在非常短的延迟后获取到你想要的数据（不超过1s）；  
2.ES的集群是去中心化的，也就是说，不像Hadoop这种分布式框架，ES集群不存在单点故障。ES集群中包含多个节点，节点可以通过选举选出它们的中心节点，因此，当集群中的一个节点出现故障时，集群马上会选取出下一个新的中心节点来管理集群；  
3.ES的横向扩展性能非常好，集群维护者不用担心集群出现资源不够的情况，因为你只需要增加一台服务器，然后在其上安装ES然后简单进行配置，这台新的节点就能成为集群中的一员；  
4.ES提供了分片机制（Shard），一个索引（Index）可以划分为多个Shard，这些Shard分布在集群中不同的节点上，能有效提升集群的处理效率；  
5.ES为其中的数据提供了replica，确保数据的冗余存储，从而使得整个ES集群可用性大大增强，亦即当一个节点出现故障时，存储在其上的数据仍然可以在其他的节点上访问到；  
6.ES简单易用，除了为开发者和使用者提供了RESTful接口外，ES本身非常易于学习和使用，这一点在应用中你可以感受到。它的社区也十分活跃，相关的文档资料也较健全。

这些点足以让我们拥有信心在需要的时候投入ES的怀抱，当然我们还需要考虑ES的一些不足，在本人的了解范围里以及结合本人的使用经验，ES集群可能存在以下问题：  
1.脑裂问题：ES集群有可能在节点间网络通信故障时成为“裂脑人”。这是ES集群的去中心化带来的不足。我们假设这样一个场景，我们的ES集群有10个节点，它们分别在两个机房A和B，有一天机房的网络出现问题，A机房无法与B机房进行通信，这时候，ES的选举机制会被触发，A机房会选取出一个中心节点，B机房也会选取出一个中心节点，整个集群一分为二，虽然对外提供访问时仍然问题不大，但是这两个集群会出现数据不同步的问题；  
2.权限管理机制不健全：迄今为止，ES集群没有比较健全的权限管理机制，如果你需要对ES的访问和使用权限进行管理，或者你需要为ES集群提供一个前端web服务，那么你需要在后台自行实现一个权限管理机制。

## ES相关概念
我们这里只介绍ES的一些相关的术语，在此之前，我们结合关系型数据库来简单介绍一下ES的结构：
>Relational DB -> Databases -> Tables -> Rows -> Columns
Elasticsearch -> Indices   -> Types  -> Documents -> Fields

理解ES的结构本身不难，但是由于ES的这些术语在我们的圈子里已经有一些其他的受众较广的含义，所以这样一种与RDB的对比可以帮助我们理解ES的结构，ES本身可以想象成一个MySQL，ES中的Index就是数据库DB，而Type相当于数据库中的表，以此类推。

**索引Index**:在ES中，Document中的所有字段都会建立索引（这里的索引是我们平常所理解的意思，如数据库的索引），这种设定使得ES中的每个文档的每个字段都是可以直接用来搜索的。事实上，我们的数据被存储和索引在分片中，索引只是一个把一个或多个分片分组在一起的逻辑空间。

**分片Shard**:我们可以将ES中的分片Shard理解为HDFS中的文件块Block，一个完整的Index可以划分为多个Shard，然后分别存储在不同的节点上；

**类型Type**:我们能够自己定义ES中的Type，Type是Index的一个逻辑分区，每个类型都有自己的映射或者结构定义，就像传统数据库表中的列一样；

**文档Document**:如果你的Tool Kit中有OOP，那么你可以简单将Document理解为对象Object，它是ES中可被索引的基础信息单元；Type是序列化为JSON格式的数据。

**映射Mapping**:ES中的映射相当于数据库中表的定义，映射定义了字段类型，每个字段的数据类型，以及字段被ES处理的方式。映射还用于设置关联到类型上的元数据。


这里只简单介绍了ES相关的基础信息，万里长征这才是第一步，但是希望这些信息可以让我们对ES有一个比较清晰的理解，至于如何使用ES进行存储数据、查询数据以及分析数据，我们需要在实践上不断学习和参悟。

最后推荐一本书，希望能帮助到各位学习和理解ES：[Elasticsearch 权威指南](http://es.xiaoleilu.com/index.html)。
