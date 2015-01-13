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
Parses a configuration file and store the values in a globally-accessible dictionary.

Usage:
import tc_config

try:
	tc_config.read_config()
except:
	print('config error')
	
print(tc_config.config_dic)
"""

import ConfigParser, threading


CONFIG_FILE = 'TrendCrawler.config' # Config file to parse.
config_dic = {} # Publicly accessible static config dicitonary.
semaphore = threading.Semaphore() # Protection for thread-safety.
	
	
def read_config():
	""" 
	Parses the configuration file and populates config_dic with values. config_dic is emptied first.
	
	throws Exception if there is a config file error.
	"""
	global CONFIG_FILE, config_dic, semaphore
	semaphore.acquire()
	config = ConfigParser.ConfigParser()
	if len(config.read(CONFIG_FILE)) == 0:
		raise Exception('Config Error')
		
	config_dic.clear()
		
	try:
		# URL info.
		keys = ['url_target_base','url_target_port','url_target_directory']
		for key in keys:
			config_dic[key] = config.get('URLS', key)
			
		# Logging info.
		keys = ['out_file','out_file2']
		for key in keys:
			config_dic[key] = config.get('LOG', key)
			
		# Database info.
		keys = ['database', 'user', 'password', 'host']
		for key in keys:
			config_dic[key] = config.get('DATABASE', key)
			
		# Trend rules
		keys = ['minimum_length']
		for key in keys:
			config_dic[key] = config.get('TREND_RULES', key)		
			
	except ConfigParser.NoOptionError as e:
		raise Exception('Config Error: '+str(e))
			
	semaphore.release()	

