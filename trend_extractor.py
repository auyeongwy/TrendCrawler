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

import sys
from kitchen.text.converters import getwriter
import tc_config, tc_database, tc_analysis_mgr


# Format stdout for unicode output
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


tc_config.read_config() # Parse config file.
db_agent = tc_database.TCDatabase() # Database connection obj.
try:
	db_agent.connect()
except psycopg2.Error as e:
	print(e.pgerror)
	sys.exit("Database connection error.")


analysis_mgr = tc_analysis_mgr.TCAnalysisMgr()


try:
	content_ids = db_agent.get_content_ids('www.neogaf.com')
	for id in content_ids:
		content = db_agent.get_content_by_id(id)
		if content is not None:
			analysis_mgr.add_content(content[0])
			#print(analysis_mgr.v_content)
except Exception as e:
	print(e)


# Start analysis.
analysis_mgr.analyze()
print(analysis_mgr.v_result)


				
# Cleanup
db_agent.close()
