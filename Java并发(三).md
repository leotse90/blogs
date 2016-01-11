#Java并发(三)
_by:leotse_

## 返回值
我们知道，可以通过创建Runnable来创建任务，但是我们却不能通过这种方式返回值。Java因此提供了另一个接口来达到返回一个值的目的，这个接口就是Callable。Callable是一种具有类型参数的泛型，它的类型参数表示的是从call()方法中返回的值的类型，我们通过ExecutorService.submit()来调用。

```java
package com.leotse.thread;

import java.util.ArrayList;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class CallableTask implements Callable<String>{

	private int id;
	public CallableTask(int id) {
		this.id = id;
	}
	
	@Override
	public String call() throws Exception {
		return "This is task " + id;
	}
	
	public static void main(String[] args) {
		ExecutorService eService = Executors.newCachedThreadPool();
		ArrayList<Future<String>> results = new ArrayList<Future<String>>();
		for (int i=0; i<5; i ++){
			results.add(eService.submit(new CallableTask(i)));
		}
		
		for (Future<String> r : results){
			try {
				System.out.println(r.get());
			} catch (InterruptedException | ExecutionException e) {
				e.printStackTrace();
			} finally {
				eService.shutdown();
			}
		}
	}

}
```
这个例子向我们展示了Callable的用法。Callable中的call()相当于Runnable中的run()方法。  
Future就是对于具体的Runnable或者Callable任务的执行结果进行取消、查询是否完成、获取结果。可以通过get方法获取执行结果，get()方法会阻塞直到任务返回结果。  

我们在这里对比一下Callable与Runnable的一些主要区别：
>1.Callable接口提供了call()方法，Runnable接口提供了run()方法；  
2.call()有返回值，run()方法没有返回值；  
3.call()可以抛出受检查的异常，run()则不能抛出受检查的异常。

## 线程休眠
有时候，我们在程序中，需要线程等待一段时间，我们可以通过sleep()方法通知Thread暂停指定的时间。线程的休眠相对比较简单，还是来看一个例子：

```java
public class SleepTask implements Runnable{

	private int id;
	
	public SleepTask(int id) {
		this.id = id;
	}
	
	@Override
	public void run() {
		System.out.println("Task " + id + ", currentTimeMillis is " + System.currentTimeMillis());
	}

	public static void main(String[] args) {
		for (int i=0; i<5; i++){
			Thread t = new Thread(new SleepTask(i));
			t.start();
			try {
				Thread.sleep(2 * 1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
}
```
得到的结果如下：
```
Task 0, currentTimeMillis is 1452526404372
Task 1, currentTimeMillis is 1452526406373
Task 2, currentTimeMillis is 1452526408373
Task 3, currentTimeMillis is 1452526410374
Task 4, currentTimeMillis is 1452526412375
```
这样的时间比较难以辨认，你可以使用Date类打印标准化时间，以便更加直观看到sleep()的效果。

## 线程的优先级
我们在并发程序中启动了多个线程，但是这些线程并不一定在重要程度上一样，我们用线程的**优先级**来定义线程的重要程序。线程的优先级意味着不同级别的线程占用CPU的概率不同，优先级低的线程不会不执行。一般来说，程序中的优先级都以默认的优先级来运行，线程的优先级可以通过getPriority()方法来获取。但是一般不建议控制线程的优先级，因为调度器的行为并不可控。

## 线程让步
我们在上一篇[博客](http://leotse90.com/2016/01/07/Java-concurrency2/)中介绍Thread的时候提到了yield()方法，该方法的作用是告诉当前线程：嘿，你已经用了CPU一段时间了，是时候让出CPU了。但是这只是一种建议，而不是一种保证。一般来说，对于任何重要的控制或在调整应用时，都不能指望yield()方法能达成我们的目的。

## 后台线程
如果在应用中，我们需要进行网络请求，或者我们需要执行一些不太重要的事情，这些任务就可以放在后台线程中。后台线程（Daemon）并不是程序中不可或缺的部分，所以如果程序中所有的非后台线程都已经结束，那么程序就已经执行结束，同时会kill掉所有的后台线程。换言之，只要有任何非后台线程还在运行状态，程序就不会结束。

如果要指定一个线程为Daemon线程，只需调用setDaemon()方法即可，如：
```java
thread.setDaemon(true);
```

**当程序中最后一个非后台线程终止运行，后台线程就会突然终止，因此一旦main()退出，JVM就会立即关闭所有的后台进程。**

