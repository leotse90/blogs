#ElasticSearch - match VS match_phrase
_by:leotse_

我们以一个使用的示例开始，我们有student这个type中存储了一些学生的基本信息，我们分别使用match和match_phrase进行查询，我们得到如下结果：  
首先，使用match。
```
GET /test/student/_search
{
  "query": {
    "match": {
      "description": "He is"
    }
  }
}
```
执行这条查询，得到的结果如下：
```
{
   "took": 3,
   "timed_out": false,
   "_shards": {
      "total": 5,
      "successful": 5,
      "failed": 0
   },
   "hits": {
      "total": 4,
      "max_score": 0.2169777,
      "hits": [
         {
            "_index": "test",
            "_type": "student",
            "_id": "2",
            "_score": 0.2169777,
            "_source": {
               "name": "februus",
               "sex": "male",
               "age": 24,
               "": "He is passionate.",
               "interests": "reading, programing"
            }
         },
         {
            "_index": "test",
            "_type": "student",
            "_id": "1",
            "_score": 0.16273327,
            "_source": {
               "name": "leotse",
               "sex": "male",
               "age": 25,
               "description": "He is a big data engineer.",
               "interests": "reading, swiming, hiking"
            }
         },
         {
            "_index": "test",
            "_type": "student",
            "_id": "4",
            "_score": 0.01989093,
            "_source": {
               "name": "pascal",
               "sex": "male",
               "age": 25,
               "description": "He works very hard because he wanna go to Canada.",
               "interests": "programing, reading"
            }
         },
         {
            "_index": "test",
            "_type": "student",
            "_id": "3",
            "_score": 0.016878016,
            "_source": {
               "name": "yolovon",
               "sex": "female",
               "age": 24,
               "description": "She is so charming and beautiful.",
               "interests": "reading, shopping"
            }
         }
      ]
   }
}
```
而当你执行match_phrase时：
```
GET /test/student/_search
{
  "query": {
    "match_phrase": {
      "description": "He is"
    }
  }
}
```
结果如下：
```
{
   "took": 3,
   "timed_out": false,
   "_shards": {
      "total": 5,
      "successful": 5,
      "failed": 0
   },
   "hits": {
      "total": 2,
      "max_score": 0.30685282,
      "hits": [
         {
            "_index": "test",
            "_type": "student",
            "_id": "2",
            "_score": 0.30685282,
            "_source": {
               "name": "februus",
               "sex": "male",
               "age": 24,
               "description": "He is passionate.",
               "interests": "reading, programing"
            }
         },
         {
            "_index": "test",
            "_type": "student",
            "_id": "1",
            "_score": 0.23013961,
            "_source": {
               "name": "leotse",
               "sex": "male",
               "age": 25,
               "description": "He is a big data engineer.",
               "interests": "reading, swiming, hiking"
            }
         }
      ]
   }
}
```

占的篇幅有点长，但是如果能基于此看清这两者之间的区别，那也是值得的。

我们分析一下这两者结果的差别：  
>1.非常直观的一点，对于同一个数据集，两者检索出来的结果集数量不一样；
2.对于match的结果，我们可以可以看到，结果的Document中description这个field可以包含“He is”，“He”或者“is”；
3.match_phrased的结果中的description字段，必须包含“He is”这一个词组；
4.所有的检索结果都有一个_score字段，看起来是当前这个document在当前搜索条件下的评分，而检索结果也是按照这个得分从高到低进行排序。

我们要想弄清楚match和match_phrase的区别，要先回到他们的用途：  
match是全文搜索，也就是说这里的搜索条件是针对这个字段的全文，只要发现和搜索条件相关的Document，都会出现在最终的结果集中，事实上，ES会根据结果相关性评分来对结果集进行排序，这个相关性评分也就是我们看到的_score字段；总体上看，description中出现了“He is”的Document的相关性评分高于只出现“He”或“is”的Document。（至于怎么给每一个Document评分，我们会在以后介绍）。
>相关性(relevance)的概念在Elasticsearch中非常重要，而这个概念在传统关系型数据库中是不可想象的，因为传统数据库对记录的查询只有匹配或者不匹配。

那么，如果我们不想将我们的查询条件拆分，应该怎么办呢？这时候我们就可以使用match_phrase：  
match_phrase是短语搜索，亦即它会将给定的短语（phrase）当成一个完整的查询条件。当使用match_phrase进行搜索的时候，你的结果集中，所有的Document都必须包含你指定的查询词组，在这里是“He is”。这看起来有点像关系型数据库的like查询操作。

相信到这里，我们都能比较清楚的理解这两者的区别。但是我们还有一个问题没有弄清楚，那就是_score到底是怎么得出的？为什么同样包含了“He is”这个phrase，_id为2的Document得分为0.30685282，而_id为1的Document的得分为0.23013961？

查询语句会为每个Document计算一个相关性评分_score，评分的计算方式取决于不同的查询类型。ES的相似度算法为TF/IDF（检索词频率/反向文档频率）。我们在这里顺带介绍一下TF/IDF的几个相关概念：

1.**字段长度准则**：这个准则很简单，字段内容的长度越长，相关性越低。我们在上面的两个例子中都能看到，同样包含了“He is”这个关键字，但是"He is passionate."的相关性评分高于"He is a big data engineer."，这就是因为字段长度准则影响了它们的相关性评分；

2.**检索词频率准则**：检索关键字出现频率越高，相关性也越高。这个例子中没有比较明显的体现出来，你可以自己试验一下；

3.**反向Document频率准则**：每个检索关键字在Index中出现的频率越高，相关性越低。

一般的，我们理解了以上三个准则，就能了解ES的相关性评分的基本守则。以下是一些相关性评分的Tips：
>单个查询可以使用TF/IDF评分标准或其他方式。如果多条查询子句被合并为一条复合查询语句，那么每个查询子句计算得出的评分会被合并到总的相关性评分中。

因为“相关性评分”这个概念和这篇博文的“相关性评分”并不高，因此在此就不展开讨论，只是点到为止，如果想要了解更多有关ES相关性评分的内容，可以自行Google，也可以继续关注我的博客，以后会专门探讨这一块内容。

