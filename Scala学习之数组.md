# Scala学习之数组

_by:leotse_

## 概述
我们从这里开始接触Scala中的数据结构，我们首先来看最基础却非常有用的数据结构——数组。  
这里会涉及两种数组：定长数组以及可变数组，顾名思义，定长数组就是数组在声明的时候就固定了大小，而可变数组可以根据我们使用的实际情况进行调整数组的长度。在Scala中，定长数组为Array，而可变数组为ArrayBuffer。

## 定长数组
我们先来看定长数组。声明一个定长数组有以下两种方式：  
**1.声明数组的类型与长度**
```scala
scala> val arr1 = new Array[Int](4)
arr1: Array[Int] = Array(0, 0, 0, 0)
```
可以看到我们用`new`关键字来声明一个Array对象，用来存储4个Int类型的数值，而这4个Int类型的数值初始值都为0。想必这点大家都很容易理解，类似的，String类型的初始值为null，Double类型的初始值为0.0。  

**2.声明数组时直接提供初始值**
```scala
scala> val arr2 = Array(2, 3, 5, 6)
arr2: Array[Int] = Array(2, 3, 5, 6)

scala> val arr3 = Array(2, "hello")
arr3: Array[Any] = Array(2, hello)
```
我们在这种声明方式中，无需使用`new`关键字，Scala会根据初始值的类型来推断出数组的类型，当数组存在多种类型时，此时数组的类型为这多种类型的最近公共父类。

另外，我们在这里还可以注意到，我们在声明数组的时候使用了关键字`val`，即数组为常量，但是实际上，这里的数组元素都是可以改变值的。这时候，我们可以将`val`定义的数组理解为：我们用`val`来指定arr1这个容器只能用来存储4个Int类型的数字，多了不行，其他类型的也不行，但是这4个Int类型的数字究竟是什么，声明方表示并不关心。

我们用`(location)`来访问数组中的元素。并且可以直接赋值给数组中的元素：
```scala
scala> arr2(0)
res12: Int = 2

scala> arr2(0) = 0

scala> arr2
res14: Array[Int] = Array(0, 3, 5, 6)
```

## 可变数组
有时候，我们在一开始声明的时候只知道我们需要数组这种容器，但是具体要放多少数据我们暂且不知道，这时候我们需要用到可变数组（又称为数组缓冲）ArrayBuffer。ArrayBuffer的声明和Array并没有太大的差异：
```scala
scala> val arrbuf1 = new ArrayBuffer[Int]
arrbuf1: scala.collection.mutable.ArrayBuffer[Int] = ArrayBuffer()

scala> val arrbuf2 = ArrayBuffer(1, 2, 3)
arrbuf2: scala.collection.mutable.ArrayBuffer[Int] = ArrayBuffer(1, 2, 3)

scala> val arrbuf3 = ArrayBuffer(1, "hello")
arrbuf3: scala.collection.mutable.ArrayBuffer[Any] = ArrayBuffer(1, hello)
```
和数组Array一样，可变数组也使用`(location)`来访问数组的元素；并且，ArrayBuffer使用`+=`来添加元素，使用`++=`来实现对其他集合的扩展。
```scala
scala> arrbuf2(0)
res18: Int = 1

scala> arrbuf2(0) = 0

scala> arrbuf2
res20: scala.collection.mutable.ArrayBuffer[Int] = ArrayBuffer(0, 2, 3)

scala> arrbuf2 += 5
res21: arrbuf2.type = ArrayBuffer(0, 2, 3, 5)

scala> arrbuf2 ++= Array(8, 9, 10)
res22: arrbuf2.type = ArrayBuffer(0, 2, 3, 5, 8, 9, 10)
```
其他的一些有关Array以及ArrayBuffer的操作，可以去ScalaDoc上查阅，你可以点击[Array](http://www.scala-lang.org/api/current/#scala.Array)或者[ArrayBuffer](http://www.scala-lang.org/api/current/#scala.collection.mutable.ArrayBuffer)。

## 总结
我们到此了解了数组的基本声明和使用方式，关于数组的具体使用需要根据实际需求进行选择。数组的有关知识也不是这几十行文字和代码所能表达得清楚的，以后的博文中会继续介绍Scala中其他的数据结构以及数组的其他的特性。