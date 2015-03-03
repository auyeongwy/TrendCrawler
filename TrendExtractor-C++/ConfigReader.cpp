#include <exception>
#include <boost/property_tree/ini_parser.hpp>
#include <list>
#include "ConfigReader.hpp"
#include "TEException.hpp"



void ConfigReader::init()
{
	boost::property_tree::ini_parser::read_ini("TrendExtractor.config", v_tree);	
}


string ConfigReader::get_value(string p_key)
{
	return v_tree.get<string>(p_key);
}



void ConfigReader::check_keys()
{
	list<string> keys;
	list<string>::iterator iter;
	
	keys.push_back("DATABASE.database");
	keys.push_back("DATABASE.user");
	keys.push_back("DATABASE.password");
	keys.push_back("DATABASE.host");
	
	for(iter=keys.begin(); iter!=keys.end(); iter++) {
		if(v_tree.find(*iter) == v_tree.not_found()) {
			string msg = *iter+" not in config.";
			throw new TEException(msg);
		}
	}
}



string ConfigReader::get_connect_db_string()
{
	string connect_str = "hostaddr='"+get_value("DATABASE.host")+"' connect_timeout='5' application_name='trendextractor' dbname='"+get_value("DATABASE.database")+"' user='"+get_value("DATABASE.user")+"' password='"+get_value("DATABASE.password")+"'";

	return connect_str;
}
