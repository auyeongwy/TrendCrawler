/*
Copyright 2015 Au Yeong Wing Yau

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
*/

#ifndef DBMGR_HPP
#define DBMGR_HPP

#include <string>
#include <libpq-fe.h>

using namespace std;

class DBMgr
{
public:
	/**
	 Connects to the database. Database parameters are configured in the config file and accessed by ConfigReader.
	 @throws exception if there is an error.
	 */
	void connect();
	
	
	/**
	 Closes connection to the database.
	 */
	void close();
	
	
	bool runSQL(string p_sql);
	
private:
	PGconn *v_conn = NULL;
};

#endif
