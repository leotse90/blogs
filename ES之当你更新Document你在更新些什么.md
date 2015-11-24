# ES之当你更新Document，你在更新些什么？
_by:leotse_

## 怎么更新ElasticSearch中的Document？
在ES中更新数据的场景有很多，比如我们要修改一个用户的年龄、爱好，又或者我们需要实时同步MySQL中的数据到ES中。我们都有修改已经存在的Document的需求。ES本身提供了两种方法让我们修改一个Document的数据，我们假设我们想要修改的内容如下：
```
GET /test/customer/1/_source

{
   "name": "yolovon",
   "age": 24
}
```
我们想将yolovon女神的年龄修改到真实年龄18岁。我们可以进行以下两种方法：  
1.使用PUT，就像我们插入数据时那样：
```
PUT /test/customer/1
{
  "name": "yolovon",
  "age": 18
}

{
   "_index": "test",
   "_type": "customer",
   "_id": "1",
   "_version": 2,
   "created": false
}
```
这里需要注意的是，我们必须将所有的字段全部输入一次，如果你只在PUT的body里输入我们要更新的字段（比如在这里我们只传入age的值），那么新的Document的就会变成我们后面PUT进去的样子（即只有age一个字段）。  
另外，我们可以看到这里的返回信息有用以标示该document唯一性的`_index`，`_type`，`_id`，以及`_version`表明该document的更新版本，`created`表明这个不是新建的而是已经存在的document。

2.使用POST，update模式更新Document：
```
POST /test/customer/1/_update
{
  "doc": {
    "age": 20
  }
}
```
你会看到这样的结果：
```
{
   "_index": "test",
   "_type": "customer",
   "_id": "1",
   "_version": 3
}
```
这时候，我们的document也变为了：
```
{
   "name": "yolovon",
   "age": 20
}
```
这里的`age`已经变成了20。而且在这里，我们只针对需要修改的`age`字段进行操作，而其他字段并不需要关心。


## 更新操作都干了些什么？
那么，在更新的时候到底发生了什么？上面的两种更新策略又有什么区别？  

我们知道，在Elasticsearch中，document是不可变的。  
>Documents in Elasticsearch are immutable; we cannot change them. Instead, if we need to update an existing document, we reindex or replace it.

这样一来，我们在更新Document时到底是怎么实现的？  
在ES中，不管我们用以上哪种方式进行更新document，它都不是真正地对原来的document进行操作。而是先将原来的document标记为删除状态，然后重新新增一个document（也就是我们看到的新的document），实际上，原来的document并没有立即消失，只是你已经不能访问它了，ES稍后会在后台真正地删除原来的document。

不管我们用那种方式进行更新，ES都会按照以下的步骤进行更新：
>1.查询出旧的document；  
2.修改document中的字段；  
3.删除旧的document；  
4.重新索引一个新的document。

但是两者还是有区别的，当使用`PUT`一个完整的document时，它需要请求两次，一次`get`请求和一次`index`请求，而使用`POST`进行`_update`操作的时候只需要一次`_udpate`请求即可。

因此我们在使用的时候，尽量避免使用`PUT`进行document的更新，特别是当我们需要批量地修改ES数据时。