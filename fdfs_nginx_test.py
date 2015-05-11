#coding=utf-8

import os
import sys
import time

# constants
FDFS_HOST = u"192.168.9.230"
FDFS_IP = 9096

def download_file_by_nginx(file_id, download_file_path):
	src_url = u"http://{host}:{port}/{file_id}".format(host=FDFS_HOST, port=FDFS_IP, file_id=file_id)
	file_name = file_id.split("/")[-1]

	start_time = time.time()
	ret = os.system(u"wget {src_url}".format(src_url=src_url))
	end_time = time.time()

	duration = end_time - start_time

	return ret == 0, duration

if __name__ == "__main__":
	file_id = sys.argv[1]
	download_file_path = u"/home/leotse/test/"

	failed_count = 0
	duration_list = []
	for i in range(50):
		ret, duration = download_file_by_nginx(file_id, download_file_path)
		duration_list.append(duration)
		if not ret:
			failed_count += 1

	print "===========================result================================"
	print "download file", str(len(duration_list)), "times"
	print "failed", str(failed_count), "times"
	print "rate of failed download:", str(1.0 * failed_count / len(duration_list) * 100), "%"
	print "average download duration:", str(sum(duration_list) / len(duration_list))
	print "================================================================="
