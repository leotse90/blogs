# 【译】Python中yield关键字用法
译：LeoTse

本文译自stackoverflow [What does the yield keyword do in Python?](http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python)

## 引子
这一切始于一位童鞋在Stack Overflow上问的问题：

Python中的yield关键字是用来干嘛的？它都干了些什么？

例如，我试图理解下面这段代码：

`def node._get_child_candidates(self, distance, min_dist, max_dist):`  
`    if self._leftchild and distance - max_dist < self._median:`  
`        yield self._leftchild`  
`    if self._rightchild and distance + max_dist >= self._median:`  
`        yield self._rightchild  `  

下面是调用代码：

`result, candidates = list(), [self]`  
`while candidates:`  
`    node = candidates.pop()`  
`    distance = node._get_dist(obj)`  
`    if distance <= max_dist and distance >= min_dist:`  
`        result.extend(node._values)`  
`    candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))`  
`return result`  

当_get_child_candidates函数被调用时发生了什么？返回了一个list？返回了单个元素？还是它再次被调用了？后面的调用什么时候停止呢？

下面是这个问题的精华回复：

## yield关键字用法

要想理解yield关键字，首先你得理解什么是**生成器**。而在这之前我们先得了解迭代。  

### 迭代

当你创建了一个list，你就可以逐个元素去读取这个list，这就叫做迭代：

`>>> mylist = [1, 2, 3]`  
`>>> for i in mylist:`  
`...    print(i)`  
`1`  
`2`  
`3`  

mylist就是可迭代的。当你使用list表达式，你就创建了一个list，亦即创建了一个迭代器：  

`>>> mylist = [x*x for x in range(3)]`  
`>>> for i in mylist:`  
`...    print(i)`  
`0`  
`1`  
`4`  
 
Python中所有你可以用到"for...in..."表达式的地方都是可迭代的：list，string，files等等。迭代器的优点是你可以读你所需，但是你需要在内存中存储（这些迭代器中的）所有的值，而当我们拥有大量数据时我们并不希望这样做。

### 生成器

生成器亦即迭代器，但是生成器只能迭代一次。因为它并不会将所有的数据存在内存中，而是实时生成我们所需的数据：

`>>> mygenerator = (x*x for x in range(3))`  
`>>> for i in mygenerator:`  
`...    print(i)`  
`0`  
`1`  
`4`  

这个和你用元组()取代列表[]道理一样。但是，你不能指望`for i in mygenerator`运行第二次，因为生成器只能被使用一次：它（首先）计算得到0，然后会遗忘0并计算得出1，最终得到4（并遗忘1），以此类推。

### yield关键字

Yield关键字和return的用法一样，只是（用到yield的）函数将会返回一个生成器。

`>>> def createGenerator():`  
`...    mylist = range(3)`  
`...    for i in mylist:`  
`...        yield i*i`  
`...`  
`>>> mygenerator = createGenerator() # create a generator`  
`>>> print(mygenerator) # mygenerator is an object!`  
`<generator object createGenerator at 0xb7555c34>`  
`>>> for i in mygenerator:`  
`...     print(i)`  
`0`  
`1`  
`4`  

这个例子不是太好。但是当你发现你的函数要返回大量只需读一次的数据时你会体会到它（yield）的好处。

要想掌握yield关键字，你必须知道：当你调用这个函数时，函数体里的代码并没有执行，它只是**返回一个生成器对象**，这看起来有点难以理解。

接着，每次你用到这个生成器的时候你的代码都会运行一次。

现在最难的部分来了：

当你第一次调用函数返回的生成器时，它将会运行函数中的代码直到执行到yield，然后它将返回这个循环产生的第一个值。接下来，每一次调用都将执行函数中的这个循环一次，并返回下一个值，直到没有值可以返回为止。

生成器会在函数执行但是没有遇到yield的情况下置空，这可能是因为循环结束了，或者是不再满足"if/else"条件。

### 问题中的代码解释

**生成器**：

`# 在这里你创建了node对象的一个返回生成器的函数`  
`def node._get_child_candidates(self, distance, min_dist, max_dist):`  
``  
`  # 下面这段代码将会在每次你使用这个生成器时被调用：`  
``  
`  # 如果node对象仍然有一个左child`  
`  # 而且distance满足条件，则返回下一个左child`  
`  if self._leftchild and distance - max_dist < self._median:`  
`      yield self._leftchild`  
``  
`  # 如果node对象仍然有一个右child`  
`  # 而且distance满足条件，则返回下一个右child`  
`  if self._rightchild and distance + max_dist >= self._median:`  
`      yield self._rightchild`  
``  
`  # 如果这个函数运行到这里了，意味着这个生成器可以看成空的了。`  
`  # 亦即：再也没有符合条件的左右child了`  

**调用方**：

`# 创建一个空的list和一个包含当前对象引用的list`  
`result, candidates = list(), [self]`  
``  
`# 循环处理candidates (最初只有一个元素)`  
`while candidates:`  
``  
`    # 获取最后一个candidate将其移除`  
`    node = candidates.pop()`  
``  
`    # 获取obj和candidate之间的距离`  
`    distance = node._get_dist(obj)`  
``  
`    # 如果距离合适，保存结果在result中`  
`    if distance <= max_dist and distance >= min_dist:`  
`        result.extend(node._values)`  
``  
`    # 将candidate的子节点保存在candidates中`  
`    # 该循环会一直循环直到遍历了所有的子节点。`  
`    candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))`  
``  
`return result`  

这段代码包含了以下几个很有意思的地方：

1）这个循环在遍历一个list，而这个list会在遍历的过程中增大。虽然存在变成无限循环的风险，但是这仍不失为遍历嵌套数据的好方法。在这里，candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))方法获取了这个生成器的所有元素，但是`while`在产生新的生成器，它们就会继续生产新的元素，直到换了一个节点。

2）extend()方法是list的一个用于将迭代器的元素追加在list中。  
一般地，我们传一个list给它：

`>>> a = [1, 2]`  
`>>> b = [3, 4]`  
`>>> a.extend(b)`  
`>>> print(a)`  
`[1, 2, 3, 4]`  

但是在你给出的代码里，它获取了一个生成器，它有如下几个好处：
a.你不需要两次读取这些元素；
b.如果你有很多子节点，你不需要把它们都保存在内存中；
这个方法很管用，因为Python不关心你传入的参数是不是一个list。Python只关心参数是否是可迭代的如字符串、list、元组以及生成器。这叫做[鸭子类型](http://zh.wikipedia.org/zh-cn/%E9%B8%AD%E5%AD%90%E7%B1%BB%E5%9E%8B)，这也是Python为何如此赞的一个原因。但是这些都不在我们的讨论范围内。


你可以到此结束，也可以接着看下面生成器的一些高级用法：

### 控制生成器

`>>> class Bank(): # let's create a bank, building ATMs`  
`...    crisis = False`  
`...    def create_atm(self):`  
`...        while not self.crisis:`  
`...            yield "$100"`  
`>>> hsbc = Bank() # when everything's ok the ATM gives you as much as you want`  
`>>> corner_street_atm = hsbc.create_atm()`  
`>>> print(corner_street_atm.next())`  
`$100`  
`>>> print(corner_street_atm.next())`  
`$100`  
`>>> print([corner_street_atm.next() for cash in range(5)])`  
`['$100', '$100', '$100', '$100', '$100']`  
`>>> hsbc.crisis = True # crisis is coming, no more money!`  
`>>> print(corner_street_atm.next())`  
`<type 'exceptions.StopIteration'>`  
`>>> wall_street_atm = hsbc.create_atm() # it's even true for new ATMs`  
`>>> print(wall_street_atm.next())`  
`<type 'exceptions.StopIteration'>`  
`>>> hsbc.crisis = False # trouble is, even post-crisis the ATM remains empty`  
`>>> print(corner_street_atm.next())`  
`<type 'exceptions.StopIteration'>`  
`>>> brand_new_atm = hsbc.create_atm() # build a new one to get back in business`  
`>>> for cash in brand_new_atm:`  
`...    print cash`  
`$100`  
`$100`  
`$100`  
`$100`  
`$100`  
`$100`  
`$100`  
`$100`  
`$100`  
`...`  

如果想要控制对资源的访问，这将非常受用。

### itertools，你上佳的朋友

itertools模块包含了操纵迭代的一些特殊的函数。你是不是曾经想过复制一个生产器？串联两个生成器？抑或在线性时间内将嵌套list中的元素分组？或者不依赖创建新list的情况下map/zip？

那么，你只要导入itertools模块就行了。

想要看个例子？让我们看看四匹马到达终点的可能顺序：

`>>> horses = [1, 2, 3, 4]`  
`>>> races = itertools.permutations(horses)`  
`>>> print(races)`  
`<itertools.permutations object at 0xb754f1dc>`  
`>>> print(list(itertools.permutations(horses)))`  
`[(1, 2, 3, 4),`  
` (1, 2, 4, 3),`  
` (1, 3, 2, 4),`  
` (1, 3, 4, 2),`  
` (1, 4, 2, 3),`  
` (1, 4, 3, 2),`  
` (2, 1, 3, 4),`  
` (2, 1, 4, 3),`  
` (2, 3, 1, 4),`  
` (2, 3, 4, 1),`  
` (2, 4, 1, 3),`  
` (2, 4, 3, 1),`  
` (3, 1, 2, 4),`  
` (3, 1, 4, 2),`  
` (3, 2, 1, 4),`  
` (3, 2, 4, 1),`  
` (3, 4, 1, 2),`  
` (3, 4, 2, 1),`  
` (4, 1, 2, 3),`  
` (4, 1, 3, 2),`  
` (4, 2, 1, 3),`  
` (4, 2, 3, 1),`  
` (4, 3, 1, 2),`  
` (4, 3, 2, 1)]`  


### 理解迭代的内部机制

迭代是实现迭代（实现了\_\_iter\_\_()函数）和迭代器（实现了\_\_next\_\_()函数）的过程。你可以从可迭代对象上获取一个迭代器，而迭代器是你可以迭代的对象。

想要了解更多，你可以看看这篇[文章](http://effbot.org/zone/python-for-statement.htm)。