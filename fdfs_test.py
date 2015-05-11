#coding=utf-8

import time

from fdfs_client.client import *
from md5mgr import mkmd5fromfile

# constants
CLIENT_CONF = u"/etc/fdfs/client.conf"


def upload_file_to_fdfs(file_path):
	client = Fdfs_client(CLIENT_CONF)
	file_md5 = mkmd5fromfile(file_path)

	start_time = time.time()
	rt_upload = client.upload_by_filename(file_path)
	end_time = time.time()
	duration = end_time - start_time
	
	file_id = rt_upload["Remote file_id"].replace("\\", "/")
	file_size = rt_upload["Uploaded size"]

	return file_md5, duration, file_id, file_size

def download_file_from_fdfs(file_id, download_file_path):
	client = Fdfs_client(CLIENT_CONF)

	start_time = time.time()
	rt_download = client.download_to_file(download_file_path, file_id)
	end_time = time.time()
	duration = end_time - start_time

	file_md5 = mkmd5fromfile(download_file_path)

	return file_md5, duration

def delete_file_from_fdfs(file_id):
	client = Fdfs_client(CLIENT_CONF)

	start_time = time.time()
	rt_delete = client.delete_file(file_id)
	end_time = time.time()
	duration = end_time - start_time

	return rt_delete, duration

if __name__ == "__main__":
	file_path = u"/home/xiefeng/test/test.mp4"
	download_file_path = u"/home/xiefeng/test/download_test.mp4"

	failed_cnt = 0
	upload_duration_list = []
	download_duration_list = []

	for i in range(1000):
		upoload_file_md5, upload_duration, file_id, file_size = upload_file_to_fdfs(file_path)
		download_file_md5, download_duration = download_file_from_fdfs(file_id, download_file_path)
		rt_delete, delete_duration = delete_file_from_fdfs(file_id)
		upload_duration_list.append(upload_duration)
		download_duration_list.append(download_duration)

		if upoload_file_md5 != download_file_md5:
			failed_cnt += 1

	aver_upload_duration = sum(upload_duration_list) / len(upload_duration_list)
	aver_download_duration = sum(download_duration_list) / len(download_duration_list)
	test_count = len(upload_duration_list)

	print "==============================result=================================="
	print "file size:", file_size
	print "upload files", str(test_count), "times"
	print "failed upload", str(failed_cnt), "times"
	print "rate of failed upload:", str(1.0 * failed_cnt / test_count * 100), "%"
	print "upload average duration:", str(aver_upload_duration), "s"
	print "download average duration:", str(aver_download_duration), "s"
	print "======================================================================"
