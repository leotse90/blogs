title: Android获取全局Context
date: 2017-06-07 23:33:21
tags:  Android
categories: 技术
---
_by:leotse_

在Android的开发中，我们经常需要在不同的场景中使用Context对象。比如，弹出一个Toast，启动一个Service或者一个Activity等等。

每个开发者都有自己的方法去获取Context，比较常见的是将Context作为一个参数传递到需要使用的方法，这种方法虽然可以实现这个目的，但是也存在着弊端，Context作为参数传递固然ok，但是需要我们在需要使用到Context的方法里都加上一个参数，这种做法并不优雅。

这时候我们有另一种办法去实现我们的目的，那就是在Application中定义一个静态方法，用以获取Context：

```java
public class MyApplication extends Application {

    private static Context cxt;

    @Override
    public void onCreate() {
        super.onCreate();

        cxt = getApplicationContext();
    }

    public static Context getContext(){
        return cxt;
    }

}
```

<!-- more -->
这样我们就可以在project的任意地方通过调用
```java
MyApplication.getContext();
```
来获取Context对象。

