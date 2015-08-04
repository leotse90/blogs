# SSH免密码登录设置
__整理：LeoTse__

## SSH免密码登录设置
准备工作：  
两台机器S1，S2。IP分别为IP1，IP2，用户名为user。  
我们想从S1免密码登录S2机器。以下为SSH设置的步骤：

Step1：生产key。在S1上输入：  
`ssh-keygen -t rsa`  
然后一直enter，直到结束。

Step2: 我们进入到~/.ssh目录，然后将生成的key通过scp复制到S2的.ssh目录（我们首先要确保目录存在）：  
`cd ~/.ssh`  
`scp ~/.ssh/id_rsa.pub user@IP2:/home/user/.ssh/IP2`  
截至目前，S1上的配置已经完成。

Step3：接下来我们登录S2机器。进入.ssh目录，确保authorized_keys文件存在：  
`cd ~/.ssh`  
`cat IP2 >> authorized_keys`  
SSH免登录已经设置完毕，如果是普通用户，继续往下看。

## 普通用户
对于普通用户authorized_keys的权限必须限定为600，否则普通用户无法实现无密钥访问，而ROOT用户按照默认即可实现无密码访问：  
`sudo chmod 600 authorized_keys`  

## 免密码登录验证
我们在S1上直接ssh连接S2机器，看能否免密码登录：  
`ssh IP2`
如果可以直接登录上去，则说明已经设置成功。

另，如果要设置S1和S2互相免密码登录，以上步骤在S1和S2都执行一次就好了！