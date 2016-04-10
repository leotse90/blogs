# 移动广告主要转化归因方式

_by:leotse_

## 概述
在移动互联网广告圈子里，无论你是Publisher，或者Ad Network，还是Ad Tracker，你都有必要了解移动广告的转化归因方式。

了解移动归因方式，可以帮助你窥探移动广告从投放到转化中很重要的一环，那就是如何甄别广告转化的归属。我们知道主要的移动互联网广告种类有CPM、CPC、CPA，这些不同的广告类型在转化归因上大同小异，所以在介绍具体的归因方式的时候再行说明。

首先，一般有下面四种归因方式：  
>1.Google Install Referrer（Google 安装引荐网址）  
2.Identifier Matching（标识符匹配）   
3.Fingerprint Matching（指纹匹配）   
4.Open URL with Click ID（带clickid的打开链接）
<!-- more -->

Open URL with ClickID主要用于点击归因，并不适合于安装归因，因此不在我们的讨论范围内。接下来，我们详细讨论这几种归因方式的原理以及适用范围。

## Google Install Referrer
Google Install Referrer，我们在[移动广告之GooglePlay推广流程](http://leotse90.com/2016/03/21/Mobile-Ad-GooglePlay/)有过介绍，这里简单说明一下，用户点击Google Play的推广URL安装的应用，GP会在该应用启动的时候发送一个Install Referrer广播告知其推广的来源，被推广的应用会上报该referrer到广告主后台，从而确定该转化的来源。

Google Install Referrer可以用来唯一标识广告商或者广告合作伙伴，这就是它可以用来确定转化的原因，有兴趣的话，你可以使用[Google Play URL Builder](https://developers.google.com/analytics/devguides/collection/android/v3/campaigns#google-play-url-builder)生成一个带referrer的推广URL，你可以了解一下其中每一个字段的用途（前提是你能翻墙）。下面是一个referrer的示例：    
`https://play.google.com/store/apps/details?id=com.test.appname&referrer=af_tranid=com.test.appname_324a78c1-c345-5cba-7a76-bc88-aacb2318a101&pid=clicksmob_int&c=US-Android-01&click_id=cA_12487526aa_278973188a866872ac981007bc8_zl&af_siteid=1111&advertising_id=yourgaid&app-id=com.test.appname`

Google Install Referrer主要适用于Google Play应用商店推广的APP，它不适用于Android上除GP以外的应用商店（这点不难理解），而且它也仅仅在APP安装的时候才有意义。

## Identifier Matching
Android平台上常见的广告标识符有GAID（Google广告ID，可以唯一标识一台Android设备，可重置）；GAID是一种由Google Play服务提供的唯一、用户特定可重置广告ID，它会以类似于38400000-8cf0-11bd-b23e-10b96e40000d的通用唯一标识符 (UUID) 格式公开用于访问字符串形式用户广告ID的API。如：  
`https://12345.api-01.com/serve?action=click&publisher_id=100&site_id=3000&google_aid=38400000-8cf0-11bd-b23e-10b96e40000d`  
尽管我们最依赖广告标识符进行归因，但在某些情况下无法使用广告标识符。例如，不支持广告标识符以及用户从非 Google Android 应用商店下载的旧有版本。如果广告标识符不可用，我们还可以依赖以下设备标识符进行归因：Android ID（适用于Android设备的ANDROID ID是一个64位数字（十六进制字符串形式），在设备首次启动时随机生成，通常在设备生命周期内保持不变）、设备 ID（适用于Android设备的设备 ID 是一种采用小写格式值的唯一设备ID）、MAC地址（联网设备的MAC地址是一个网络地址，用于对设备的无线网络适配器进行唯一标识，采用以冒号分隔的大写形式，例如，“AA:BB:CC:DD:EE:FF”）。

iOS平台上的标识符主要就是IFA（可唯一标识一台iOS设备，但是也可以通过刷机重置）。Apple从iOS6开始引入了广告商标识符 (IFA)，它为应用提供用于为广告服务的标识符的访问权，并提供用以指示用户是否启用了Limit Ad Tracking（限制广告追踪）功能的标志。IFA 值是每台设备唯一的字母数字字符串，使用带连字符的大写形式。如：“AAAAAAAAA-BBBB-CCCC-1111-222222220000”。尽管我们最依赖广告标识符进行归因，但在某些情况下无法使用广告标识符。例如，不支持广告标识符的旧有版本。如果广告标识符不可用，我们依赖开放UDID进行归因，“开放 UDID”是iOS系统 UIDevice 类遭弃用的唯一标识符属性（又名 UDID）的简易替代者。它是一个长 40 个字符（20 个字节）的十六进制值。

标识符匹配的归因流程如下：  
1.用户点击应用上的广告。一方面，用户设备会跳转到应用市场，另一方面，设备会向Tracker发送带有包含用户设备标识符的Ad Click URL；  
2.用户点击安装广告上的应用后，应用会上报该用户设备标识符给Tracker；  
3.Tracker对比点击时上传的用户设备标识符以及用户安装后上传的设备标识符，如果一致，就可以确定这个转化的来源。

Identifier Matching不仅适用于转化的归因，同样适用于点击事件、浏览事件等，它是适用范围最广的转化归因方式。

## Fingerprint Matching
要理解Fingerprint Matching转化归因，首先你得理解什么是Fingerprint，我们可以把Fingerprint理解为可以唯一标识一个用户的基本信息（尽管很多时候并不能真正唯一映射到一个确定的用户），它可以是用户的IP地址，也可以是用户设备的可用的HTTP头，这些基本信息可以用于归因分析中创建用户的点击事件的指纹。

**当一个用户安装了一个移动应用，植入在该应用的归因分析SDK就会收集该设备的指纹信息，然后上报到归因分析平台，平台会生成一个设备指纹并有序地在匹配的指纹中查找，归因分析平台会将转化算在匹配的所有指纹中最后一次带来点击上。**

默认情况下，匹配设备指纹的归因时间窗口是24小时，因此为了找到匹配，归因分析只会考虑24小时内发生的点击事件。当然也有一些广告网络和广告伙伴、媒体声称他们能将归因窗口扩展至48小时甚至72小时，但是实际上一旦超过24小时指纹匹配的统计的精度就会下降。

当一个用户点击一个广告跳转URL，归因分析SDK会设置其HTTP cookie，用于区分唯一点击数与Gross点击（理解为毛点击数），该cookie会在24小时后失效。  
如果设备上没有设置cookie，归因分析SDK就会认定这个设备是一个从未记录在案的新设备，并记录这次点击为唯一点击和Gross点击；  
如果设备上已经设置了cookie，归因分析SDK就会认为这是一个已经存在的用户（24小时内），于是只记录这次点击为一次Gross点击，而并不会记录其为唯一点击。

归因分析中会根据Gross点击和唯一点击去判断一个用户是新增还是已经存在。如果归因分析平台认定该用户是过去24小时已经存在的用户，那么平台就不会重新创建该用户的指纹，相反的，平台将会更新指纹的更新时间为最后一次点击的时间戳。因此，用户点击多次并不会创建额外的设备指纹，从而可以降低错误匹配数。

> 关于Gross点击与唯一点击，举一个简单的例子：  
用户A点击：广告1、广告2、广告1  
用户B点击：广告1、广告3  
那么：  
广告1：2次唯一点击以及3次Gross点击；  
广告2：1次唯一点击以及1次Gross点击；  
广告3：1次唯一点击以及1次Gross点击。

指纹匹配在移动应用后台中异步运行，此方法可强制打开浏览器，不会妨碍用户体验。由于使用另外的几种归因可提供1:1的准确性，而指纹匹配取决于统计概率（大约86%的统计概率），因此另外两种归因方法始终胜过指纹匹配。

