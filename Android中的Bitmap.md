#Android中的Bitmap
_by:leotse_

## Bitmap简介
Bitmap，我们称之为位图文件，它的扩展名一般是.bmp，有时也可以是.dip。位图由点（像素）组成，其可以理解为一个像素矩阵，矩阵中的每一个点表示对应位置上像素的颜色，每个点可以由多种颜色组成，包括2，4，8，16，24，32位色彩。一张1200x628分辨率的32位真彩图片，所占的存储空间为：1200x628x32/(8x1024)＝2944KB。由于位图的构造，使得其图像效果很好好，它是非压缩格式的，但是这也导致它需要占用较大的存储空间，这让位图变得不太适合在网络上传输。

![Bitmap example](http://a.hiphotos.baidu.com/baike/w%3D268/sign=f0dd0be3533d26972ed30f5b6dfbb24f/d52a2834349b033b0b84caf317ce36d3d539bd8e.jpg)

由于Bitmap的应用比较广泛，因此Android中常常使用到Bitmap。但是在使用Bitmap的时候，我们常常需要考虑到其占用内存较大的事实，因此关注Bitmap的OOM异常成为我们使用Bitmap的必修课。我们主要需要注意以下几个方面：
>1.Android系统资源有限；  
2.Bitmap很能吃内存；  
3.应用的UI一般加载多张Bitmap，这样会一下消耗很多内存。

## Bitmap的处理
### Bitmap的加载优化
考虑我们前面讲到的Bitmap很耗内存，我们在加载Bitmap的时候就需要时时注意内存情况。在选择图片时，我们就需要知道找到一张合适的图片比一张效果好的图片更加合理（除非你的应用对图片质量要求很高，比如壁纸类应用）。这里介绍Android中的Bitmap的处理类：`BitmapFactory`。

`BitmapFactory`提供了多种decode图片的方法，比如：`decodeByteArray()`，`decodeFile()`，`decodeResource()`等等，这些方法方便我们从不同的来源创建Bitmap，这些方法都可以通过`BitmapFactory.Options`来指定decode选项，设置`inJustDecodeBounds`属性为true可以在decode时避免分配内存，它会返回一个空的Bitmap，但是我们可以获取到Bitmap的outWidth, outHeight与outMimeType。我们这样就可以在构造Bitmap之前读图片的尺寸与类型。为了避免OOM，我们在一开始就可以检查Bitmap图片的尺寸。示例代码如下：
```java
    public void checkBitmap(){
        BitmapFactory.Options mOptions = new BitmapFactory.Options();
        mOptions.inJustDecodeBounds = true;
        BitmapFactory.decodeResource(getImgResource(), R.id.mImage, mOptions);
        int mImgHeight = mOptions.outHeight;
        int mImgWidth = mOptions.outWidth;
        String mImgType = mOptions.outMimeType;
    }

    private Resources getImgResource(){}
```
我们在获取了Bitmap的尺寸后，就能很灵活地决定是否需要加载完整的Bitmap图片，如果我们在评估以下几项后决定是否需要加载一个缩小版本的图片：
>1.加载完整的Bitmap需要耗费的内存；  
2.加载这张Bitmap是否会增加其他相关的内存占用；  
3.放置这张图片的的控件尺寸是否合适；  
4.屏幕大小以及设备的屏幕密度；

在评估后如果觉得没有必要加载完整的图片就可以考虑加载缩小版的Bitmap。我们需要告诉Bitmap的解码器我们打算加载缩小版的Bitmap，这时可以在`BitmapFactory.Options`中设置`inSampleSize`的值，例如, 一个分辨率为2048x1536的图片，如果设置`inSampleSize`为4，那么会产出一个大约512x384大小的Bitmap。加载这张缩小的图片仅仅使用大概0.75MB的内存，如果是加载完整尺寸的图片，那么大概需要花费12MB（前提都是Bitmap的配置是 ARGB_8888）。下面有一段根据目标图片大小来计算Sample图片大小的代码示例：
```java
public static int calculateInSampleSize(
            BitmapFactory.Options options, int reqWidth, int reqHeight) {
    // Raw height and width of image
    final int height = options.outHeight;
    final int width = options.outWidth;
    int inSampleSize = 1;

    if (height > reqHeight || width > reqWidth) {
        final int halfHeight = height / 2;
        final int halfWidth = width / 2;
        // Calculate the largest inSampleSize value that is a power of 2 and keeps both
        // height and width larger than the requested height and width.
        while ((halfHeight / inSampleSize) > reqHeight
                && (halfWidth / inSampleSize) > reqWidth) {
            inSampleSize *= 2;
        }
    }

    return inSampleSize;
}
```
**Note**: 设置inSampleSize为2的幂是因为解码器最终还是会对非2的幂的数进行向下处理，获取到最靠近2的幂的数。详情参考`inSampleSize`的文档。
为了使用该方法，首先需要设置`inJustDecodeBounds`为true, 把options的值传递过来，然后设置`inSampleSize`的值并设置 `inJustDecodeBounds`为false，之后重新调用相关的解码方法。
```java
public static Bitmap decodeSampledBitmapFromResource(Resources res, int resId,
        int reqWidth, int reqHeight) {

    // First decode with inJustDecodeBounds=true to check dimensions
    final BitmapFactory.Options options = new BitmapFactory.Options();
    options.inJustDecodeBounds = true;
    BitmapFactory.decodeResource(res, resId, options);

    // Calculate inSampleSize
    options.inSampleSize = calculateInSampleSize(options, reqWidth, reqHeight);

    // Decode bitmap with inSampleSize set
    options.inJustDecodeBounds = false;
    return BitmapFactory.decodeResource(res, resId, options);
}
```
使用上面这个方法可以简单地加载一张任意大小的图片。如下面的代码样例显示了一个接近100x100像素的缩略图：
```java
mImageView.setImageBitmap(
    decodeSampledBitmapFromResource(getImgResources(), R.id.mImage, 100, 100));
```
类似的，我们也可以通过替换合适的`BitmapFactory`解码方法来实现一个类似的方法从其他的数据源解析Bitmap。

### Bitmap的内存优化
在Android的演变进程中，管理Bitmap内存也发生了改变。在Android 2.2及以前的版本，当GC的时候，应用的线程会被暂停，在Android2.3开始，新增了并发GC机制，**这意味着在一个Bitmap不再被引用之后，它所占用的内存会被立即回收。**   
在Android2.3.3及之前，一个Bitmap的像素级是存放在Native空间里，这些数据与Bitmap本身是隔离的，Bitmap本身被存放在Dalvik堆中，我们无法预测在Native内存中的像素级数据何时会被释放，这意味着程序容易超过它的内存限制并且崩溃。自Android 3.0开始， 像素级数据则是与Bitmap本身一起存放在Dalvik堆中。

好在我们现在Android的主流版本在Android4.0以上，因此Bitmap在不被引用后就会被回收。

>在过去，一种比较流行的内存缓存实现方法是使用软引用（SoftReference）或弱引用（WeakReference）对Bitmap进行缓存，然而我们并不推荐这样的做法。从Android 2.3开始，垃圾回收机制变得更加频繁，这使得释放软（弱）引用的频率也随之增高，导致使用引用的效率降低很多。而且在Android 3.0之前，备份的Bitmap会存放在Native Memory中，它不是以可预知的方式被释放的，这样可能导致程序超出它的内存限制而崩溃。


### Bitmap的线程操作
我们可以通过`BitmapFactory`的解码方法来获取Bitmap，但是当图片来源于网络或者其他非内存来源时，我们就需要考虑由此带来的线程问题，毕竟我们在UI线程上不适合干这件事，那么我们可以考虑使用`AsyncTask`：加载Bitmap的类继承`AsyncTask`，并重载`doInBackground()`以及`onPostExecute()`方法。开始异步加载Bitmap，只需要创建一个新的任务并执行它即可。
>为ImageView使用WeakReference确保了AsyncTask所引用的资源可以被垃圾回收器回收。由于当任务结束时不能确保ImageView仍然存在，因此我们必须在onPostExecute()里面对引用进行检查。

```java
class BitmapWorkerTask extends AsyncTask {
    private final WeakReference imageViewReference;
    private int data = 0;

    public BitmapWorkerTask(ImageView imageView) {
        // Use a WeakReference to ensure the ImageView can be garbage collected
        imageViewReference = new WeakReference(imageView);
    }

    // Decode image in background.
    @Override
    protected Bitmap doInBackground(Integer... params) {
        data = params[0];
        return decodeSampledBitmapFromResource(getResources(), data, 100, 100));
    }

    // Once complete, see if ImageView is still around and set bitmap.
    @Override
    protected void onPostExecute(Bitmap bitmap) {
        if (imageViewReference != null && bitmap != null) {
            final ImageView imageView = imageViewReference.get();
            if (imageView != null) {
                imageView.setImageBitmap(bitmap);
            }
        }
    }
}
```
我们可以按照这样异步加载Bitmap：
```java
public void loadBitmap(int resId, ImageView imageView) {
    BitmapWorkerTask task = new BitmapWorkerTask(imageView);
    task.execute(resId);
}
```

至此，我们就Android中的Bitmap进行比较全面的介绍，当然可以参考官网了解更多有关[Bitmap](http://developer.android.com/reference/android/graphics/Bitmap.html)的信息。

