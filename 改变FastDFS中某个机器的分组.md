# 改变FastDFS中某个机器的分组
_By：LeoTse_

我们假设有FastDFS集群A，B，C，D三台机器，其中A为Tracker。BCD都为Storage，它们同属group1，现在想要将C机器重新建一个group2，应该怎么操作呢？  

*step1：停止C机器上的FastDFS服务*   
`/usr/bin/stop.sh /usr/bin/fdfs_storaged /etc/fdfs/storage.conf`

*step2：将C从FastDFS集群的group1中删除*  
`/usr/bin/fdfs_monitor /usr/bin/client.conf delete group1 C_ip_addr`

*step3：修改C机器的storage.conf配置*  
`# the name of the group this storage server belongs to `   
`#  `  
`# comment or remove this item for fetching from tracker server,`  
`# in this case, use_storage_id must set to true in tracker.conf,`  
`# and storage_ids.conf must be configed correctly.`   
`group_name=group2`  

将group_name改为group2。

注意：如果Tracker为指定store_lookup方式，即tracker.conf配置中：  
`# the method of selecting group to upload files`    
`# 0: round robin`    
`# 1: specify group`    
`# 2: load balance, select the max free space group to upload file`    
`store_lookup=2`    

`# which group to upload file`    
`# when store_lookup set to 1, must set store_group to the group name`   
`store_group=group1`    

如果store_lookup=1，则需要将其修改为0或者2，酌情选择。如果store_lookup不是1，则store_group会忽略。

*step4：删除base_path下的data目录*  
这个时候要看我们是否需要删除C机器已经存储的文件。如果我们不再需要C机器上保存的文件，则可以删除base_path下data目录，重新启动FastDFS服务时会新建data目录；如果我们不想删除C机器上现有的文件，则可以删除除了存储目录以外的其他目录和文件：fdfs_storaged.pid文件、storage_stat.dat文件、.data_init_flag文件以及sync目录。

*step5：重启C机器的FastDFS服务*  
`/usr/bin/fdfs_storaged /etc/fdfs/storage.conf`  


（如果我们想要卸载FastDFS，直接删除base_path下的data目录即可。）

至此，我们对集群重新分组完成。