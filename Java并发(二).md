#Java并发(二)
_by:leotse_

## Java的线程机制
我们在上一篇[博客](http://leotse90.com/2016/01/06/Java并发(一)/)中，提到最理想的实现并发编程的方式就是使用进程，但是Java中我们使用线程进行多任务处理，原因在上一篇博客中也已经提及。

在Java中，每一个线程都会对应一个任务，这些任务构成了一个并发的程序。	在底层看来，每一个线程都觉得自己独占了CPU，虽然事实上它们只是在某一个时间切片上占有了CPU。CPU会轮流给每一个线程分配时间，这些细节一般不需要我们去了解。

### Runnable接口
我们知道，Java中的并发程序是由任务构成，那么Java中怎么声明一个任务呢？Java为我们提供了一个Runnable接口，凡是实现了Runnable接口的类皆可以称之为一个任务。下面的实例展示了Java中如何声明任务：
```java
public class MyRunnable implements Runnable {
	@Override
	public void run() {
		System.out.println("I am a task");
	}
}
```
我们看到这里有一个run()方法，我们将打算在这个任务中执行的业务逻辑都放在run()方法中。我们另行编写一个测试类用来执行这个Task。
```java
public class MyRunnableDemo {
	public static void main(String[] args) {
		MyRunnable task = new MyRunnable();
		task.run();
	}
}
```
运行的结果如下：
```
I am a task
````
这样看来，觉得Runnable和普通的Java类没有什么区别。这里只是在main()线程中执行了这个任务。如果我们希望这个任务和一个线程对应起来，应该怎么做呢？我们需要显式地将任务绑定到一个线程上。这就需要我们用到Thread类。

### Thread类
在Java中，一个Thread类的对象就是一个Java程序的执行线程。JVM允许一个程序有多个线程。每一个线程都有其优先级，高优先级的线程会先于低优先级的线程执行，想必这个很容易理解。每一个线程都可以被声明为一个后台线程。如果一个运行的线程中创建了一个新的Thread对象，那么这个新的Thread对象的初始优先级和创建它的线程一样，如果创建它的线程是一个后台线程，那么这个新的Thread对象也是一个后台线程。

当JVM启动时，通常会有一个非后台线程运行，这就是我们熟知的main线程，JVM会一直执行程序中的线程直到发生了下列情况：  
1）Runtime类的exit()方法被调用，并且安全管理器允许这个退出操作执行；  
2）所有的线程都是非后台进程，而且都已经停止运行；或者获取了run()方法调用的返回值；又或者run()抛出了一个异常。

我们在上面提到需要显示将一个任务和一个线程绑定在一起。常用的方法就是在创建一个Thread对象的时候将任务作为构造器的参数。我们将前面的MyRunnable类改造一下：
```java
public class MyRunnable implements Runnable {
	private int threadCount = 0;
	
	public MyRunnable(int count) {
		this.threadCount = count;
	}
	
	@Override
	public void run() {
		System.out.println("Thread " + threadCount);
	}

}
```
然后，我们编写另一个类MyThreadDemo来创建任务并执行：
```java
public class MyThreadDemo {
	public static void main(String[] args) {
		for (int i = 0; i < 5; i ++){
			MyRunnable task = new MyRunnable(i);
			Thread t = new Thread(task);
			t.start();
		}
		
	}
}
```
或者我们可以这样：
```java
public class MyThreadDemo {
	public static void main(String[] args) {
		for (int i = 0; i < 5; i ++){
			new Thread(new MyRunnable(i)).start();
		}
		
	}
}
```
在这里，我们创建了5个任务，并把它们分别和一个Thread对象进行绑定，然后执行这些线程，得到结果如下：
```
Thread 0
Thread 4
Thread 3
Thread 1
Thread 2
```
由于线程调度机制是非确定性的，所以每次执行的结果都可能会不同。

在Thread类中，我们需要关注以下一些主要的方法：  
**yield()**:该方法会建议调度器当前进程将要让出自己对处理器的使用，但是调度器可以选择是否需要接受这个建议。一般不建议使用这个方法，但是如果在debug或测试的时候还是可以使用的。

**sleep()**:这个方法可以短暂中断当前执行线程。我们可以指定当前执行线程的休眠时间；

**start()**:开始执行一个线程，当调用这个方法时，JVM会执行这个线程的run()方法。调用这个方法的结果就是两个线程并发执行：从这个start()方法调用返回的线程，执行run()方法的线程。需要注意的是，我们不能多次启动同一个线程，而且一个线程一旦执行结束就不能重启；阅读Thread的源码可知，start()本身是一个同步方法，且里面调用了本地方法start0()方法启动一个线程：
```java
public synchronized void start() {
    /**
     * This method is not invoked for the main method thread or "system"
     * group threads created/set up by the VM. Any new functionality added
     * to this method in the future may have to also be added to the VM.
     *
     * A zero status value corresponds to state "NEW".
     */
    if (threadStatus != 0)
        throw new IllegalThreadStateException();

    /* Notify the group that this thread is about to be started
     * so that it can be added to the group's list of threads
     * and the group's unstarted count can be decremented. */
    group.add(this);

    boolean started = false;
    try {
        start0();
        started = true;
    } finally {
        try {
            if (!started) {
                group.threadStartFailed(this);
            }
        } catch (Throwable ignore) {
            /* do nothing. If start0 threw a Throwable then
              it will be passed up the call stack */
        }
    }
}
```

**exit()**:系统调用这个方法以期让一个线程在其真正退出运行前进行资源的清理工作；

**interrupt()**:中断当前线程。但是在实际编程中，我们在使用它时需要特别注意，你可以看看这篇[博客](http://www.blogjava.net/jinfeng_wang/archive/2008/04/27/196477.html)


这些都是Java的线程机制中比较基础的，还有其他的诸如Executor以及优先级等其他概念，我们将在下一次介绍。