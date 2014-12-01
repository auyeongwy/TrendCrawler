# Copyright 2014 Au Yeong Wing Yau
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Logs info to files.

Usage:

"""

import tc_config, threading


out_file = ''
out_file2 = ''
out_fp = None
out_fp2 = None
semaphore = threading.Semaphore() # Protection for thread-safety.


def init_logger():
	""" Initializes logging. Must be called before any other function. Calling this again will re-initalize logging. """
	global out_file, out_fp, out_file2, out_fp2, semaphore
	
	semaphore.acquire()
	
	out_file = tc_config.config_dic['out_file']
	if out_fp is not None:
		out_fp.close()
	out_fp = open(out_file, 'w')
	
	out_file2 = tc_config.config_dic['out_file2']
	if out_fp2 is not None:
		out_fp2.close()
	out_fp2 = open(out_file2, 'w')
	
	semaphore.release()
	

def close_logger():
	""" Closes log file handlers. """
	global out_fp, out_fp2, semaphore
	semaphore.acquire()
	if out_fp is not None:
		out_fp.close()
		out_fp = None
		
	if out_fp2 is not None:
		out_fp2.close()
		out_fp2 = None	
	semaphore.release()
	
	
def log_out(output):
	""" Writes output to the 'out_file' file.
	param output The string to write.
	"""
	global out_fp, semaphore
	semaphore.acquire()
	out_fp.write(output)
	semaphore.release()
	
	
def log_out2(output):
	""" Writes output to the 'out_file2' file.
	param output The string to write.
	"""
	global out_fp2, semaphore
	semaphore.acquire()
	out_fp2.write(output)
	semaphore.release()	