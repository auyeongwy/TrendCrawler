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

""" Class to provide database connection. """

import psycopg2
import psycopg2.extensions
import tc_config


class TCDatabase:
	""" Class to provide database connection.
	usage:
	
	agent = tc_database.TCDatabase()
	try:
		agent.connect()
	except psycopg2.Error as e:
		# Error handling.
		
	# Use the agent object.
	agent.close() # Finished. Close connection. Note that the same "agent" can be re-used by just calling "agent.connect()" again.
	"""
	def __init__(self):
		psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
		psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
		self.v_conn = None # Database connection.
		

		
	def connect(self):
		""" Initializes connection. tc_config MUST be initialized system-wide first.
		raise Exception psycopg2.Error
		"""
		dic = tc_config.config_dic
		self.v_conn = psycopg2.connect(database=dic['database'], user=dic['user'], password=dic['password'], host=dic['host'])
		self.v_conn.autocommit = True
		

		
	def close(self):
		""" Closes the connection if it exists. Exceptions will not be raised but will be logged.
		"""
		try:
			if self.v_conn is not None:
				self.v_conn.close()
		except psycopg2.Error as e:
			print(e.pgerror)
		self.v_conn = None
		
		
		
	def get_url_id(self, p_url):
		""" Returns an id for a URL. If the URL does not exist, it will be created and a new id returned. Exceptions are logged, not raised.
		param p_url The URL to get an id.
		return Id of the URL. -1 if an error occurs.
		Throws exception for database error.
		"""
		result = -1
		try:
			cur = self.v_conn.cursor()
			cur.execute("select * from get_url_id(%s)", [p_url])
			data = cur.fetchone()
			if data[0] is not None:
				result = data[0]
		except psycopg2.Error as e:
			print(e.pgerror)
			
		return result
	
	
	
	def add_content(self, p_id, p_content):
		""" Adds parsed content to the database.
		param p_id URL id of the URL associated with the content to be added. Retrieved via get_url_id().
		param p_content Text content to be added.
		Throws exception for database error.
		"""
		try:
			cur = self.v_conn.cursor()
			cur.execute("select * from add_content(%s,%s)",[p_id,p_content])
		except psycopg2.Error as e:
			print(e.pgerror)
			
			
			
	def get_content_ids(self, p_baseurl):
		""" Retrieves all ids in content table with the specified baseurl. E.g. 'www.world.com' returns results for 'www.world.com*' (wildcard).
		param p_baseurl The base URL to search for, e.g. 'www.world.com'.
		return Python list of ids.
		"""
		try:
			p_baseurl += '%' # Append wildcard character for the 'like' SQL function.
			cur = self.v_conn.cursor()
			cur.execute("select * from get_content_ids(%s)", [p_baseurl])
			return cur.fetchall()
		except psycopg2.Error as e:
			print(e.pgerror)
		
		
		
	def get_content_by_id(self, p_id):
		""" Retrieves parsed content of the specified entry in the content table.
		param p_id Id of the content table entry to retrieve.
		return Text content.
		"""
		try:
			cur = self.v_conn.cursor()
			cur.execute("select * from get_content_by_id(%s)", p_id)
			result = cur.fetchone()
			return result
			#if result[0] is not None:
			#	return result[0]
			#else:
			#	return 
		except psycopg2.Error as e:
			print(e.pgerror)