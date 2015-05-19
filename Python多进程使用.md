# Python多进程使用

## Intro
我们知道，由于[GIL](https://wiki.python.org/moin/GlobalInterpreterLock)的关系，Python中多线程并不被看好。因此，Python我们常常使用模块subprocess模块和多进程multiprocessing模块来实现并发。而subprocess因为是调用外部程序而且只是通过管道进行文本交流，因此我们建议在Python并发编程中，尽量使用multiprocessing。  

multiprocessing模块和threading模块很像，该模块同时提供了本地和远程并发，你也不用担心GIL产生的副作用。并且multiprocessing可以在Unix和Windows下使用（区别于为shell而生的subprocess）。

## multiprocessing使用
在multiprocessing模块中，我们使用multiprocessing.Process()来创建一个新的进程对象。

一般情况下，我们需要在创建Process对象时指定进程执行的函数，以及该函数的参数：  
`process = multiprocessing.Process(target=worker, args=(param1, param2)`  
该对象的主要方法有：  
**start()**：启动进程；每个进程最多只能调用一次；  
**run()**：进程的执行逻辑在run()里。如果Process对象没有指定target，就会默认执行Process的run()方法；  
**join([timeout])**：阻塞当前进程，直到调用join方法的那个进程执行完，再继续执行当前进程；  
**is_alive()**：返回该进程是否存活；  
**terminate()**：终结一个进程。当调用这个函数的时候，运行逻辑中的exit和finally代码段将不会执行。而且这个进程的子进程不会被终结而是成为孤儿进程；  

下面我们给出一段多进程使用的示例代码：  
`import multiprocessing`  
`def controller():`  
`	processes = []`  
`	for i in range(5):`  
`		process = multiprocessing.Process(target=worker, args=[i])`  
`		processes.append(process)`  
`	for process in processes:`  
`		process.start()`  
`	for process in processes:`  
`		process.join()`  
`def worker(param):`  
`	print param`  
`if __name__ == '__main__':`  
`	controller()`  

我们可以得到如下的输出：  
`1`  
`0`  
`2`  
`4`  
`3`  

## 子进程通信
multiprocessing支持两种类型的进程通信手段，分别是Queue和Pipe。  
### Queue
Queue是一种多线程优先队列。它允许多个进程读和写，我们通过`mutiprocessing.Queue(maxsize)`创建一个Queue，maxsize表示队列中可以存放对象的最大数量。它的一些主要方法有：  
**get()**：删除并返回队列中的一个元素；  
**put()**: 添加元素到队列；  
**qsize()** : 返回队列中元素的个数；  
**empty()**: 队列为空返回True否则返回False；  
**full()**: 队列已满返回True，负责返回False；  

在下面的示例里，我们用Queue实现获取多进程执行时的输出：   

`import multiprocessing`  
`def controller():`  
`    processes = []`  
`    result_queue = multiprocessing.Queue()`  
`    for i in range(5):`  
`        process = multiprocessing.Process(target=worker, args=[i, result_queue])`  
`        processes.append(process)`  
`    for process in processes:`  
`        process.start()`  
`    for process in processes:`  
`        process.join()`  
`    while not result_queue.empty():`  
`        print result_queue.get()`  
`def worker(param, result_queue):`  
`    result_queue.put(param + 100)`  
`if __name__ == '__main__':`  
`    controller()`   

执行这段代码，输出为：  
`101`  
`102`  
`103`  
`100`  
`104`  

### Pipe
Pipe可以是单向，也可以是双向。我们通过mutiprocessing.Pipe(duplex=False)创建单向管道 (默认为双向)。它主要有send()和recv()两种方法，顾名思义，分别是发送消息和接受消息。  
我们同样来看一段示例代码：  
`import multiprocessing`  
`def controller():`  
`	processes = []`  
`	parent_conn, child_conn = multiprocessing.Pipe()`  
`	for i in range(5):`  
`		process = multiprocessing.Process(target=worker, args=[i, child_conn])`  
`		processes.append(process)`  
`	for process in processes:`  
`		process.start()`  
`		print parent_conn.recv()`  
`	for process in processes:`  
`		process.join()`  
`def worker(param, child_conn):`  
`	child_conn.send(param + 100)`  
`if __name__ == '__main__':`  
`	controller()`   
执行这段代码，输出为：  
`100`  
`101`  
`102`  
`103`  
`104`  


## Q&A
为什么要先依次调用start再调用join，而不是start完了就调用join呢？  
答：假设我们有两个进程p1，p2，如果我们在p1执行后先join()然后再p2.start()，我们就会发现是先执行完p1，再执行主线程，最后才开始p2。这是因为join是用来阻塞当前线程的，p1.start()之后，p1就提示主线程，需要等待p1结束才向下执行，那主线程就乖乖的等着啦，自然没有执行p2.start()。
