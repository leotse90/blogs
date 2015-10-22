# Scala之函数
_by:leotse_

今天我们来介绍Scala中的函数的一些基本概念以及用法。  

## 函数是一等公民
在Scala中，函数是一等公民。
首先来解释一下什么是_一等公民_，它指的是在程序中可无限使用的对象。  
那么”函数是Scala的一等公民“这句话怎么理解呢？一言蔽之，就是函数能作为实参，还能作为返回值，它能作为一个普通变量进行使用。详细一点来说，Scala中作为一等公民的主要表现有：  
1.可以传递和赋值
2.嵌套函数
3.匿名函数
4.高阶函数
5.闭包

## 函数
我们来正式介绍Scala中的函数，先看函数的主要构成，和其他编程语言一样，函数主要由：**函数名**、**参数**以及**函数体**三部分组成。下面我们会从这三个方面介绍Scala中的函数。下面是一个函数的示例：
<pre><code>
def foo(x: Int) = println(x)
</code></pre>

### 函数名
关于函数名，没有太多需要介绍的，和其他编程语言一样，支持数字、字母以及下划线，$符号，同样的，数字不能放在函数名第一位。一般建议，函数命名采用驼峰风格（小驼峰）。  

### 参数
接下来是参数，在Scala中，所有的参数必须指定类型。在某些情况下，函数的参数可以有默认值，我们称之为默认参数：
<pre><code>
scala> def func(x: Int, y: Int = 3) = x + y
func: (x: Int, y: Int)Int

scala> func(2)
res14: Int = 5

scala> func(2, 4)
res15: Int = 6

scala> func(1, 3, 4)
<console>:16: error: too many arguments for method func: (x: Int, y: Int)Int
       func(1, 3, 4)

scala> func(y=2, x=6)
res17: Int = 8
</code></pre>
我们需要注意，如果我们传入的参数数量和函数的参数数量不一致(不能多于函数的参数数量)，函数会从左到右依次将值传给参数。但是当你在传参时指定了参数名（带名参数），那么参数的顺序就不再重要。

如果我们的参数长度未知，这时我们可以使用**变长参数**。变长参数实际上是一个类型为Seq的参数（Seq是一个有先后顺序的值的序列，比如数组或者列表）。但是你不能直接将值的序列当成参数传给函数（特指参数为变长参数的函数）。我们看下面的代码便能明白变长参数的使用：
<pre><code>
scala> def toStr(args: String *) = args.mkString(",")
toStr: (args: String*)String

scala> toStr("leotse", "yolovon")
res20: String = leotse,yolovon

scala> toStr("One", "Two", "Three")
res21: String = One,Two,Three
</code></pre>

### 函数体
在上面的示例中，我们已经多次见过Scala中的函数，他们的函数体如果只有一个表达式或者语句，那么直接跟在函数名后即可（有等号=），如果函数体包含多条语句，那么我们可以使用我们以前介绍过的块表达式。

### 返回值
我们知道，块表达式的值为{...}中的最后一个表达式的值，那么在Scala的函数中，如果没有指定函数的返回值，块表达式的返回值就是块表达式的最后一个语句的值。**一般情况下，我们都不需要显式指定Scala函数的返回值。**当然我们也可以直接指定函数的返回值类型，如下：
<pre><code>
def func(v1: Int, v2: String): Double = {...}
</code></pre>
这里再一次说明了函数是第一等公民，因为我们直接将函数func指定了一个类型Double。

## 过程
在前面介绍函数的时候，我们看到Scala函数和其他编程语言函数定义不同的地方，那就是函数名后面加了一个等号＝。那么这个＝是不是必须的呢？答案是不。如果函数体在块表达式中而且返回值为Unit类型，那么就可以不要这里的＝，我们称这样的函数为**过程**。不过，有人建议我们一般情况下都加上＝号，并且指定函数的返回值类型，哪怕是Unit类型：  
<pre><code>
scala> def func1 (a: Int, b: Int) {
     |     println(a + b)
     | }
func1: (a: Int, b: Int)Unit

scala> func1(2, 5)
7

scala> def func2 (a: Int, b: Int): Unit = {
     |     println(a + b)
     | }
func2: (a: Int, b: Int)Unit

scala> func2(4, 5)
9
</code></pre>

Scala的函数基础知识暂且告一段落，但是只有多动手试试才能对Scala的函数有更深层次的理解。