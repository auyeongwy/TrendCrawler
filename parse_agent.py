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

""" Class to parse and filter HTML content. """
import re


class ParseAgent:
	""" Class to extract HTML string. To see usage, refer to the testing code included below. """
	BODY_PATTERN = '<body[^>]*>.*</body>' # Regex to extract the form <body>*</body>.
	TAG_PATTERN = '<([A-Za-z]+[^>]*)>([^<]+)' # Regex to extract the form <tag>capture<, to be applied recursively.
	CONTENT_PATTERN = '[^\s\n\r]' # Find any non white-space, non-newline content.
	
	
	
	def __init__(self):
		""" Initializes the object. """
		self.v_re_body = re.compile(ParseAgent.BODY_PATTERN, re.DOTALL | re.IGNORECASE | re.UNICODE) # RE that implents BODY_PATTERN.
		self.v_re_tag = re.compile(ParseAgent.TAG_PATTERN, re.UNICODE) # RE that implements TAG_PATTERN.
		self.v_re_content = re.compile(ParseAgent.CONTENT_PATTERN, re.UNICODE) # RE that implements CONTENT_PATTERN
		self.v_match_obj = None # Current MatchObj returned by the most recent operation. None if no match.
		self.v_data = '' # Current string data that is being searched.
		self.v_match = '' # Current match data.
	
	
	
	def init_body(self, input):
		""" Initializes the string to search through. This automatically extracts the <body>content</body> part into v_data.
		param input Input string to search through.
		return True if successful. False if failed or the <body>content</body> pattern does not exist in input.
		"""
		self.v_match_obj = self.v_re_body.search(input) # Extract the <body>content</body> part.
		if self.v_match_obj is not None:
			self.v_data = self.v_match_obj.group(0)
			return True
		else:
			return False
			
	
	
	def get_content(self):
		""" Retrieves the content from the form <anytag>content</anytag> in v_data - which is initialized if init_body() returns True. The content is written to v_match. At the same time the match is truncated from v_data. So calling get_content() recursively keeps returning content until there is none to retrieve.
		return True if successful and the content is written to v_match. False if nothing to match.
		"""
		while True:
			res = self.get_tag_content()
			if res == 1:
				if self.v_match_obj.group(1).lower().startswith('script') is False: # Ignore script tag.
					return True
			elif res == -1:
				return False
				
		
		
	def get_tag_content(self):
		"""
		Extract content from the form <tag>content<can be other tag>.
		self.v_data is where the whole HTML resides. MatchObject is written to self.v_match_obj. Matched content is written into self.v_match.
		"""
		self.v_match_obj = self.v_re_tag.search(self.v_data)
		if self.v_match_obj is not None:
			self.v_match = self.v_match_obj.group(2) # The match.
			self.v_data = self.v_data[self.v_match_obj.end():] # Prune out the matched data.
			if self.verify_content() is True:
				return 1
			else:
				return 0
		return -1
		
		
		
	def verify_content(self):
		"""
		After extracting content from <tag>content<tag> into self.v_match, verify content is not just useless whitespace. Also prune any newlines in content.
		This function will operate on self.v_match.
		return True if content is OK, else False.
		"""
		match_obj = self.v_re_content.search(self.v_match)
		if match_obj is not None:
			#remove special chars
			#self.v_match = self.v_match.replace('\u000A',' ') # Linebreak '\n'
			self.v_match = self.v_match.replace('\n',' ') # Linebreak '\n'
			#self.v_match = self.v_match.replace('\u000D','') # Windows return '\r'
			self.v_match = self.v_match.replace('\r','') # Windows return '\r'
			#self.v_match = self.v_match.replace('\u0009',' ') # tab '\t'
			self.v_match = self.v_match.replace('\t',' ') # tab '\t'
			return True
		else:
			return False
			
			
			
# Testing code
if __name__ == "__main__":
	re_agent = ParseAgent()
	input = '<html><body><data>text</data>\n<data>text2\n\r</data></body></html>'
	print(input)
	match = False
	if re_agent.init_body(input) is True:
		while re_agent.get_content() is True:
			print(re_agent.v_match)
			match = True
			
	if match is False:
		print('no match')
