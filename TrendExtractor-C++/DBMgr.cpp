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

#include "DBMgr.hpp"
#include "ConfigReader.hpp"
#include "TEException.hpp"


void DBMgr::connect()
{
	ConfigReader cr;
	this->close(); /* Ensure connection is clean. */
	v_conn = PQconnectdb(cr.get_connect_db_string().c_str());
	if(v_conn == NULL)
		throw TEException("Fatal error: Connection problem.");
	if(PQstatus(v_conn) != CONNECTION_OK) {
		PQfinish(v_conn);
		throw TEException("Fatal error: Connection problem.");
	}
}



void DBMgr::close()
{
	if(v_conn != NULL) {
		PQfinish(v_conn);
		v_conn = NULL;
	}
}



bool DBMgr::runSQL(string p_sql)
{
	PGresult *result = PQexec(v_conn, p_sql.c_str());
	if(result != NULL) {
		if(PQresultStatus(result) == PGRES_TUPLES_OK) {
			int row = PQntuples(result);
			int column = PQnfields(result);
			int i, j;
			for(i=0; i<column; i++)
				cout << PQfname(result, i) << " ";
			cout << endl;
			for(i=0; i<row; i++) {
				for(j=0; j<column; j++) {
					cout << PQgetvalue(result, i, j) << " ";
				}
				cout << endl;
			}
		}
		else
			return false;
		
		PQclear(result);
		return true;
	}
	else
		return false;
}