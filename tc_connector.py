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


""" HTTP connector that connects and communicates with the target. """
import httplib, StringIO, gzip, re
import tc_connection_target



class TCConnector:
	""" HTTP connector that connects and communicates with the target.
	
	Usage:
	import tc_connector, tc_connection_target
	
	conn_target = tc_connection_target.TCConnectionTarget()
	... (fill in conn_target with appropriate values)...
	conn = tc_connector.TCConnector(conn_target)
	response_string = conn.request()
	....(other stuff)....
	conn.close() # Cleanup.
	"""
	
	
	# HTTP headers to use.
	HEADERS_DIC = {"User-Agent":"Mozilla/5.0", "Accept":"text/html", "Accept-Language":"en-gb,en;q=0.5", "Accept-Encoding":"gzip,deflate"}
	DOMAIN_PATTERN = 'http://([^/]+)'



	def __init__(self, p_connection_target):
		""" Initializes the object.
		param p_connection_target A valid TCConnectionTarget object.
		"""
		self.v_conn_target = p_connection_target
		self.v_re_domain = re.compile(TCConnector.DOMAIN_PATTERN)
		self.v_conn = httplib.HTTPConnection(self.v_conn_target.v_domain, self.v_conn_target.v_port, self.v_conn_target.v_timeout)
		self.v_response = None
		self.v_response_headers = None
		self.v_re_charset = re.compile("charset=\s*([^\s\n\r]+)", re.IGNORECASE)
		self.v_charset = ''
		
		
		
	def close(self):
		""" Closes the connection. Recommend to call even if request() was not called on the TCConnector. """
		print('Disconnecting: '+self.v_conn_target.v_domain+self.v_conn_target.v_directory)
		self.v_conn.close()
		
		
		
	def get_current_url(self):
		return self.v_conn_target.v_domain+self.v_conn_target.v_directory
		
		
		
	def request(self):
		""" Makes the HTTP request and returns the response.
		
		return The body of the HTTP response in a 'unicode' type.
		raises Exception if anything that isn't '200 OK' or HTTP error occured.
		"""
		try:
			print('Connecting: '+self.get_current_url())
			self.v_conn.request("GET", self.v_conn_target.v_directory, headers=TCConnector.HEADERS_DIC)
			self.v_response = self.v_conn.getresponse()
			stat = self.v_response.status
			print('Response: '+str(stat))
			
			if stat == 200:
				return self.process_response()
			elif stat == 301 or stat == 303:
				return self.redirect_request()
			else:
				raise Exception('Unhandled HTTP response: '+str(stat))
		
		except httplib.HTTPException as e:
			raise Exception(e.strerror)
		
		
	
	def redirect_request(self):
		"""
		Handles re-direct responses by disconnecting current connection and connecting to the re-directed location. 
		This actually calls self.request() again after configuring the corrent parameters in self.
		
		param p_http_response httpresponse object containing the 3xx redirect response.
		return Value returned by self.request().
		raise Exception for unexpected errors.
		"""
		self.close() # Close current connection.
		location = self.v_response.getheader('location')
		match_obj = self.v_re_domain.search(location)
		if match_obj is not None:
			self.v_conn_target.v_domain = match_obj.group(1)
			self.v_conn_target.v_directory = location[match_obj.end():]
			self.v_conn = httplib.HTTPConnection(self.v_conn_target.v_domain, self.v_conn_target.v_port, self.v_conn_target.v_timeout)
			return self.request()
		else:
			raise Exception('Unhandled redirect location: '+self.v_response.getheaders())
		
		
		
	def process_response(self):
		""" Process the response from the HTTP request.
		return The body of the HTTP response in 'unicode' type.
		raises Exception if HTTP error occured.
		"""
		self.v_response_headers = self.v_response.getheaders()
		data = self.get_data()
		return data
		

	
	def get_data(self):
		""" Get data from the HTTP response. In particular, perform uncompression if 'content-encoding:gzip' is set in the HTTP response header.
		return HTTP body data in 'unicode' type.
		raises Exception if HTTP error occured.
		"""
		gzipped = False
		for header_pair in self.v_response_headers: # Find the 'content-encoding' header.
			if(header_pair[0].lower() == 'content-encoding'):
				if header_pair[1].startswith('gzip'):
					gzipped = True
					
			elif(header_pair[0].lower() == 'content-type'): # Find "content-type" header to determine charset.
				match_obj = self.v_re_charset.search(header_pair[1])
				if match_obj is not None:
					#self.v_charset = match_obj.group(1).lower()
					self.v_charset = match_obj.group(1).lower()
					print('CHARSET IS '+self.v_charset)
				else:
					raise Exception('Received invalid charset')

		# Retrieve the body data.
		data = self.v_response.read()
		
		# Uncompress if body is compressed.
		if gzipped is True:
			compressedstream = StringIO.StringIO(data)
			gzipper = gzip.GzipFile(fileobj=compressedstream)
			data = gzipper.read()

		# Decode the data. Before decode it is 'str' type, becoming 'unicode' type after decode.
		#print('BEFORE DECODE: '+str(type(data))) 
		data = data.decode(self.v_charset)
		#print('AFTER DECODE: '+str(type(data)))
		
		return data
