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
from kitchen.text.converters import getwriter
import tc_config, tc_logger, parse_agent, tc_connection_target, tc_connector, tc_database


# Format stdout for unicode output
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


tc_config.read_config() # Parse config file.
#tc_logger.init_logger() # Initialize logging handlers.
agent = parse_agent.ParseAgent() # Parsing agent.
conn_target = tc_connection_target.TCConnectionTarget() # Connection details.
conn_target.v_domain = tc_config.config_dic['url_target_base']
conn_target.v_directory = tc_config.config_dic['url_target_directory']



db_agent = tc_database.TCDatabase() # Database connection obj.
try:
	db_agent.connect()
except psycopg2.Error as e:
	print(e.pgerror)
	sys.exit("Database connection error.")
conn = tc_connector.TCConnector(conn_target) # HTTP connection obj.



try:
	data = conn.request()
	res = db_agent.get_url_id(conn.get_current_url())
	if res != -1:
		#tc_logger.log_out(data)
		if agent.init_body(data) is True:
			while agent.get_content() is True:
				print(agent.v_match)
except Exception as e:
	print(e)
				
				
# Cleanup
#tc_logger.close_logger()
conn.close()
db_agent.close()
