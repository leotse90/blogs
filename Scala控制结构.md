# Scala控制结构
_by:leotse_

### 块表达式
首先，我们需要了解一下块表达式。我们这样定义块表达式：凡是用{}包含的语句都同属一个块表达式，在Scala中，块表达式的值等于块表达式最后一条语句的值（在Scala中，每一个表达式都有一个值）。我们看下面的示例：  
<pre><code>
scala> var v = {var a = 2; var b = 4; a + b;}
v: Int = 6
scala> val v1 = {var s1 = "hello"; var i = 20;}
v1: Unit = ()
</code></pre>

在这里，我们可以总结以下两点：1.块表达式的值由{...}中的最后一条语句的值决定，那么当我们在定义一个函数的时候，一般不需要定义返回值，因为最后一条语句的值就是这个块表达式的值；2.侧面反映了Scala中赋值语句的值为Unit类型（注：Scala中的Unit类型相当于Java中的void，其只有一个值()）。  

### 条件表达式
条件表达式的作用就不赘述，我们直接来介绍Scala中的条件表达式。它的一般形式如下：  
`if (expression) block1 else block2`  
值得注意的是，Scala虽然和Java一样，判断条件expression需要为Boolean类型，但是和其他一些语言不一样的是，在Scala中，只有真正的Boolean类型：true或者false能作为判断的依据，而正整数、非空字符串等不能表示true，同理，整数0、空字符串等亦不能表示false。看下面的代码：  
<pre><code>
scala> if (1) 1 else -1
<console>:11: error: type mismatch;
 found   : Int(1)
 required: Boolean
       if (1) 1 else -1
           ^

scala> if ("") 1 else -1
<console>:11: error: type mismatch;
 found   : String("")
 required: Boolean
       if ("") 1 else -1
           ^
</code></pre>

在Scala中，我们可以将条件表达式的值直接赋给一个变量：  
<pre><code>
scala> val r = if ("hello" > "world") "hello" else "world"
r: String = world
</code></pre>

这种用法熟悉Python的coder可能会比较容易接受，Scala这种设计可能会使得代码在阅读起来并没有那么友善，但是确实可以使得我们的代码更简洁。

另外，Scala并不支持switch语句，因此如果我们有模式匹配上的需求，我们需要用到Scala提供的更强大的模式匹配机制，感兴趣的朋友可以先行了解一下。

### 循环表达式
和Java一样，Scala提供了两种循环表达式：while以及for。  
通常，函数式语言会避开while循环，因为while实现的大多数操作都可以使用递归来完成。Scala中while循环和Java类似：  
<pre><code>
scala> var x = 3
x: Int = 3

scala> while (x > 0) {
     |     println(x)
     |     x -= 1
     | }
3
2
1
</code></pre>

Scala中的for循环却和Java中的不太一样，在形式上有较大的改变，有一种观点认为：“Scala 的for实际上是一条管道，它在将元素传递给循环主体之前处理元素组成的集合，每次一个。此管道其中的一部分负责将更多的元素添加到管道中（生成器），一部分负责编辑管道中的元素（过滤器），还有一些负责处理中间的操作（比如记录）。”：  
<pre><code>
scala> for (i <- 1 to 4) print(i + " ")
1 2 3 4 
</code></pre>  
这段代码等同于：  
<pre><code>
scala> for (i <- 1 to 4) {
     |     print(i + " ")
     | }
1 2 3 4 
</code></pre>

这里我们看到`for (i <- 1 to 4)`这种形式的表达式，这条表达式的意思是我们从1到4进行一个遍历，然后将这些值依次赋予变量i。更普遍的for定义是`for (v <- expression)`，也就是将expression每次生成的值赋给变量v。我们看到**在for循环的变量v之前并没有var或者val，此时，v的类型是集合的元素类型。**

这种循环便利非常方便，比如我们要遍历一个字符串：  
<pre><code>
scala> for (c <- "hello, scala") print(c + "-")
h-e-l-l-o-,- -s-c-a-l-a-
</code></pre>

我们还可以这样遍历其他诸如数组、集合之类。

for循环表达式还有更加先进的使用方法，我们称之为_for推导式_。还是先看一段代码：  
<pre><code>
scala> for (i <- 1 to 2; j <- 1 until 3) println((i, j))
(1,1)
(1,2)
(2,1)
(2,2)

scala> for (i <- 1 to 2; j <- 1 until 3 if i != j) println((i, j))
(1,2)
(2,1)
</code></pre>
我们需要解释一下这段代码，首先额外解释一下to和until的区别，x to y表示从x到y的所有整数，包含y；而x until y表示从x到y的所有整数不包含y（y > x）。我们在这段代码看到，for循环的循环控制语句中有多条表达式，并且以分号分割，每个表达式我们称之为**生成器**，生成器的作用是在每一次循环的时候生成变量的值，控制变量j的赋值语句后跟着`if i != j`，这是一个**守卫**，守卫用以过滤符合条件的控制变量。


到这里为止，我们已经对Scala的控制结构有一个大致的了解。在实际编码中，我们会看到更灵活、更强大的控制结构使用方法，但是万变不离其宗，它们都是基于这些基本的控制结构形式。