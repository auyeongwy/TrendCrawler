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

import sys, httplib
import tc_config, tc_logger, parse_agent, tc_connection_target, tc_connector


tc_config.read_config() # Parse config file.
#tc_logger.init_logger() # Initialize logging handlers.
re_agent = parse_agent.ParseAgent() # Parsing agent.

conn_target = tc_connection_target.TCConnectionTarget() # Connection details.
conn_target.v_domain = tc_config.config_dic['url_target_base']
conn_target.v_directory = tc_config.config_dic['url_target_directory']

conn = tc_connector.TCConnector(conn_target) # Connector class.


try:
	data = conn.request()
	#tc_logger.log_out(data)
	if re_agent.init_body(data) is True:
		while re_agent.get_content() is True:
			print(re_agent.v_match)
except Exception as e:
	print(e)
				
				
# Cleanup
#tc_logger.close_logger()
conn.close()

