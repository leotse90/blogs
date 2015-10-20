# Scala入门
_by:leotse_

### 为什么是Scala
有人问Java之父James Gosling“除了Java语言以外，您现在还使用JVM平台上的哪种编程语言？”，他毫不犹豫的回答“Scala”。

`During a meeting in the Community Corner (java.net booth) with James Gosling, a participant asked an interesting question:"Which Programming Language would you use now on top of JVM, except Java?". The answer was surprisingly fast and very clear: - Scala.`

可见，Scala是一门很受待见的编程语言，另一位大牛Horstmann指出，Scala试图将以下三组对立的思想融合在一门编程语言中：  
`－函数式编程 VS 面向对象编程`  
`－富有表达力的语法 VS 静态类型`  
`－高级的语言特性 VS 与Java高度集成`  
这样看来，Scala就是想集各家所长，打造一种平衡的和谐，这看起来像是编程语言世界的乌邦托。  
Scala和很多在Java基础上发展的语言一样，需要基于JVM，这一点使得Scala拥有强大的Java所拥有的特性，比如跨平台。但是成也JVM，败也JVM，JVM启动较慢的问题，需要编译等等这些也成为了Scala的瓶颈。只要还立足于JVM，Scala就一直会受到JVM的限制。

但是这些都无碍于Scala本身成为一门成功的语言，现在很多公司都已经逐渐投靠Scala阵营，比如twitter，特别是当使用Scala编写的Spark兴起之后，Scala更是成为很多公司大数据编程语言的首选。

### Scala & REPL
首先，我们需要认识一下REPL，全称为Read-Eval-Print-Loop，亦即读取－求值－打印－循环。如果是第一次接触这个概念，会觉得有点奇怪，我们可以将REPL称为**交互式解释器**。一般的，我们通过REPL可以快速学习和验证一门语言的特性（前提是这门语言支持REPL）。  
但是并不是所有的语言都支持REPL，常见的编程语言支持REPL的有Ruby、Python、Lua，使用很广的Java、C++、C#、PHP以及JS等并不支持原生的REPL。当然，我们既然在这里讨论REPL，Scala是肯定支持REPL的。我们在学习Scala的时候可以直接在REPL coding。实际上，我们敲进去的代码首先被编译，然后JVM会执行编译后的字节码，然后返回执行的结果。

我们看一个示例：  
`scala> "Hello, Scala"`   
`res0: String = Hello, Scala`   
从这个示例中，我们可以看到输入的是文本“Hello, Scala”，下面一行是输出，这里的res0是REPL为这个文本起的名字，后面的String表明这个文本是字符串类型。我们可以直接使用res0这个变量名去调用这个字符串文本。

### 变量声明：val和var
在上一小节里面，我们已经见识到了Scala的变量声明，但是，我们一般情况下都希望将变量命名的权力牢牢控制在自己手上，因此我们可以使用以下方式声明变量。
－var：variable的缩写。用法如下：  
`var variable_name: [variable_type] = variable_value`  
变量的类型是可选的，因为如果没有指定变量的类型，Scala的编译器会根据变量的值推断出它的类型。我们看下面的示例：

`scala> var x: Int = 1  // 指定x的类型为Int`  
`x: Int = 1`  
`scala> x = 2  // 改变变量x的值`  
`x: Int = 2`  
`scala> var y = 3  // 没有指定y的类型`  
`y: Int = 3`

－val：这里说变量其实不太准确，因为val声明的是不可变的常量。使用方法和var类似，只是不能修改它的值。在实际开发中，除非我们可以预知需要改变一个值的内容，否则我们一般用val声明。示例如下：  

`scala> val z = 3`  
`z: Int = 3`  
`scala> z = 2  // 不可以修改一个常量的值`  
`<console>:11: error: reassignment to val`

一般的，我们不需要声明类型，除非必须。而且我们注意到Scala和Java等语言不一样，变量的类型声明在变量名后面。

另外，我们在REPL中的示例中可以看到，解释器为我们没有命名的变量定义res0这个名字，凡是解释器定义的变量，如res0、res1等等，都是常量，不可修改:  
`scala> res0`  
`res1: String = Hello, Scala`  
`scala> res0 = 1990`  
`<console>:11: error: reassignment to val`

在Scala中，有8种类型，它们分别为Boolean、Byte、Char、Short、Int、Long、Float以及Double。在这里，我们和Java那样称它们为八大基本类型，因为Scala中并不会刻意去区分基本类型和引用类型，因为他们都是类。


### 参考资料  
《快学Scala》Cay S. Horstmann 电子工业出版社   
《深入理解Scala》 Joshua D. Suereth 人民邮电出版社   
[Scala官方API](http://www.scala-lang.org/api/current/#package)   
[Scala官方Tutorials](http://docs.scala-lang.org/tutorials/?_ga=1.213857492.1110750532.1444722905)   
[Scala中文社区](http://www.scalachina.com)   
网上前辈们学习交流的技术博客与论坛