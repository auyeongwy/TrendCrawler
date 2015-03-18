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

#include <exception>
#include <boost/property_tree/ini_parser.hpp>
#include <list>
#include "ConfigReader.hpp"
#include "TEException.hpp"


void ConfigReader::init()
{
	v_mtx.lock();
	boost::property_tree::ini_parser::read_ini("TrendExtractor.config", v_tree);
	check_keys();
	v_mtx.unlock();
}


string ConfigReader::get_value(string p_key)
{
	return v_tree.get<string>(p_key);
}



void ConfigReader::check_keys()
{
	list<string> keys;
	list<string>::iterator iter;
	string tmp;
	
	/* List mandatory list of keys to check here. */
	keys.push_back("DATABASE.database");
	keys.push_back("DATABASE.user");
	keys.push_back("DATABASE.password");
	keys.push_back("DATABASE.host");
	//keys.push_back("DUMMY");
	
	/* Check mandatory list of keys. Throw an exception if a value is missing. */
	try {
		for(iter=keys.begin(); iter!=keys.end(); iter++) {
			tmp = get_value(*iter);
		}
	} catch(exception &e) {
		throw new TEException(*iter + " not in config.");
	}
}



string ConfigReader::get_connect_db_string()
{
	string connect_str = "hostaddr='"+get_value("DATABASE.host")+"' connect_timeout='5' application_name='trendextractor' dbname='"+get_value("DATABASE.database")+"' user='"+get_value("DATABASE.user")+"' password='"+get_value("DATABASE.password")+"'";

	return connect_str;
}
