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


/** 
 * @file TrendExtractor.cpp
 * Contains main() function of TrendExtractor, provides higest level control of the application.
 */
#include <iostream>
#include <list>
#include <utility>
#include <string>
#include <iostream>
#include <stdlib.h>
#include "ConfigReader.hpp"
#include "DBMgr.hpp"


using namespace std;


static void do_abort();

/* Initialise static variables. */
boost::property_tree::ptree ConfigReader::v_tree;
boost::mutex ConfigReader::v_mtx; 


/**
 * The main() function.
 */
int main()
{
	ConfigReader configReader;
	DBMgr dbMgr;
	
	try {
		configReader.init();
		dbMgr.connect();
		bool result = dbMgr.runSQL("select * from urls");
		if(!result)
			cout << "SQL problem" << endl;
		dbMgr.close();
	} catch (exception *e) {
		cout << e->what() << endl;
		do_abort();
	}

	
	return 0;
}



/**
 * Aborts the application when a fatal error occurs.
 */
static void do_abort()
{
	cout << "Fatal error, aborting." << endl;
	abort();
}
