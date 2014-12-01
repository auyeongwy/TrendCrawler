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
		self.v_conn = httplib.HTTPConnection(self.v_conn_target.v_domain, self.v_conn_target.v_port, self.v_conn_target.v_timeout)
		self.v_re_domain = re.compile(TCConnector.DOMAIN_PATTERN)
		
		
		
	def close(self):
		""" Closes the connection. Recommend to call even if request() was not called on the TCConnector. """
		print('Disconnecting: '+self.v_conn_target.v_domain+self.v_conn_target.v_directory)
		self.v_conn.close()
		
		
		
	def request(self):
		""" Makes the HTTP request and returns the response.
		
		return The body of the HTTP response in a string object.
		raises Exception if anything that isn't '200 OK' or HTTP error occured.
		"""
		try:
			print('Connecting: '+self.v_conn_target.v_domain+self.v_conn_target.v_directory)
			self.v_conn.request("GET", self.v_conn_target.v_directory, headers=TCConnector.HEADERS_DIC)
			res = self.v_conn.getresponse()
			print('Response: '+str(res.status))
			
			if res.status == 200:
				return self.process_response(res)
			elif res.status == 301 or res.status == 303:
				return self.redirect_request(res)
			else:
				raise Exception('Unhandled HTTP response: '+str(res.status))
		
		except httplib.HTTPException as e:
			raise Exception(e.strerror)
		
		
	
	def redirect_request(self, p_http_response):
		"""
		Handles re-direct responses by disconnecting current connection and connecting to the re-directed location.
		param p_http_response httpresponse object containing the 3xx redirect response.
		return Retrieved HTTP document.
		raise Exception for unexpected errors.
		"""
		self.close() # Close current connection.
		location = p_http_response.getheader('location')
		match_obj = self.v_re_domain.search(location)
		if match_obj is not None:
			self.v_conn_target.v_domain = match_obj.group(1)
			self.v_conn_target.v_directory = location[match_obj.end():]
			self.v_conn = httplib.HTTPConnection(self.v_conn_target.v_domain, self.v_conn_target.v_port, self.v_conn_target.v_timeout)
			return self.request()
		else:
			raise Exception('Unhandled redirect location: '+p_http_response.getheaders())
		
		
		
	def process_response(self,p_http_response):
		""" Process the response from a HTTP request.
		return The body of the HTTP response in a string object.
		raises Exception if HTTP error occured.
		"""
		
		# Check response encoding.
		gzipped = False
		res_headers = p_http_response.getheaders() # Returns a list of tuples.
		for header_pair in res_headers: # Find the 'content-type' header.
			if(header_pair[0].lower() == 'content-encoding'):
				if header_pair[1].startswith('gzip'):
					gzipped = True
				break
				
		data = p_http_response.read()
		if gzipped is True: # A compressed body is returned. Need to uncompress it.
			compressedstream = StringIO.StringIO(data)
			gzipper = gzip.GzipFile(fileobj=compressedstream)
			data = gzipper.read()

		return str(data)