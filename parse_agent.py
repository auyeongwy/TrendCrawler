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
	BODY_RE = '<body[^>]*>.*</body>' # Regex to extract the form <body>*</body>.
	TAG_RE = '</?([A-Za-z]+)[^>]*>([^<]+)' # Regex to extract the form <tag>capture<, to be applied recursively.
	CONTENT_RE = '[^\s\n\r]' # Find any non white-space, non-newline content.
	SKIPPED_TAGS = 'script|style' # Tags to skip.
	HREF_RE = 'href="([^"]+)"' # Find href reference.
	CLEAN_WHITESPACE = '\s+' # Pattern to cancel consecutive whitespace.
	CLEAN_SPECIAL_CHARS_RE = '\n|\t' # Pattern to locate all '\n' and '\t'
	CLEAN_WHITESPACE_RE = '\s+' # Pattern to cancel consecutive whitespace.
	
	
	
	def __init__(self):
		""" Initializes the object. """
		self.v_re_body = re.compile(ParseAgent.BODY_RE, re.DOTALL | re.IGNORECASE | re.UNICODE)
		self.v_re_tag = re.compile(ParseAgent.TAG_RE, re.UNICODE)
		self.v_re_content = re.compile(ParseAgent.CONTENT_RE, re.UNICODE)
		self.v_re_skipped_tags = re.compile(ParseAgent.SKIPPED_TAGS, re.UNICODE)
		self.v_re_href = re.compile(ParseAgent.HREF_RE, re.UNICODE)
		self.v_re_clean_whitespace = re.compile(ParseAgent.CLEAN_WHITESPACE, re.UNICODE)
		self.v_re_clean_special_chars = re.compile(ParseAgent.CLEAN_SPECIAL_CHARS_RE, re.UNICODE)
		self.v_re_clean_whitespace = re.compile(ParseAgent.CLEAN_WHITESPACE_RE, re.UNICODE)		
		self.v_data = '' # Current string data that is being searched.
		self.v_match = '' # Current match data.
		self.v_url_list = [] # List of URLs from the document content.
	
	
	
	def init_body(self, input):
		""" Initializes the string to search through. This automatically extracts the <body>content</body> part into v_data.
		param input Input string to search through.
		return True if successful. False if failed or the <body>content</body> pattern does not exist in input.
		"""
		self.v_match = '' # Make sure to clear out any matches.
		self.v_url_list = []
		match_obj = self.v_re_body.search(input) # Extract the <body>content</body> part.
		if match_obj is not None:
			self.v_data = match_obj.group(0)
			self.clean_whitespace()
			return True
		else:
			return False
			
	
	
	def get_content(self):
		""" 
		Parses v_data and extracts all HTML text content into v_match.
		"""
		self.clean_whitespace() # Clean up unnecessary whitespace and special characters.
		while True:
			match_obj = self.v_re_tag.search(self.v_data)
			if match_obj is not None:
				index = self.verify_tag(match_obj.group(1))
				if index == 0:
					self.v_match += match_obj.group(2)+' '
					self.v_data = self.v_data[match_obj.end()-1:]
				else:
					self.v_data = self.v_data[index:]
			else:
				break
				
		self.v_match = self.v_re_clean_whitespace.sub(' ', self.v_match) # Remove redundant consecutive whitespace in final v_match.
		
		
		
	def verify_tag(self, p_tag):
		"""
		Verify if the tag obtained is approved. 
		param p_tag The tag obtained.
		return 0 if the tag is approved. If the tag is not approved returns the index that the index in v_data where the search point should be moved to skip everything in the non-approved tag.
		"""
		match_obj = self.v_re_skipped_tags.search(p_tag)
		if match_obj is None:
			if p_tag == u'a': # If the tag is a hyperlink, get the URL.
				self.get_href()
			return 0
		else:
			end_tag_re = re.compile('</'+p_tag+'[^>]*>', re.UNICODE | re.IGNORECASE)
			match_obj = end_tag_re.search(self.v_data)
			if match_obj is not None:
				return match_obj.end()
			else:
				return len(v_data)-1
		
		
		
	def get_href(self):
		"""
		Extracts the 1st href encountered in v_data and appends it to v_url_list.
		"""
		match_obj = self.v_re_href.search(self.v_data)
		if match_obj is not None:
			self.v_url_list.append(match_obj.group(1))
			
			

	def clean_whitespace(self):
		"""
		After extracting content into self.v_data, clean up redundant spaces such as newlines, tags, consecutive whitespace, etc.
		"""
		self.v_data = self.v_data.replace('\r','') # Windows return '\r'
		self.v_data = self.v_re_clean_special_chars.sub(' ', self.v_data) # Change all '\t' and '\n' to whitespace.
		self.v_data = self.v_re_clean_whitespace.sub(' ', self.v_data) # Remove redundant consecutive whitespace.
		
			
			
			
# Testing code
if __name__ == "__main__":
	re_agent = ParseAgent()
	#input = '<html><body><data>text</data>\n<data>text2\n\r</data></body></html>'
	input = '<html><body><h2>Welcome to NeoGAF</h2><p>NeoGAF is a nexus of hardcore gamers, enthusiast press, and video game industry developers and publishers. This is a neutral ground where facts and evidence, presented within the confines of civil, inclusive discourse, prevail through careful moderation. Enjoy reading existing discussions as a guest, or <a href="register.php$session[sessionurl_q]">sign up</a> for a free account and be patient through the waiting period.</p></body></html>'

	match = False
	if re_agent.init_body(input) is True:
		match = True
		#re_agent.clean_whitespace()
		re_agent.get_content()
		print(re_agent.v_match)
		
	if match is False:
		print('no match')
