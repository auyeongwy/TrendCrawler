#ifndef CONFIGREADER_HPP
#define CONFIGREADER_HPP

#include <string>
#include <boost/property_tree/ptree.hpp>


using namespace std;

/**
 * Provides access to config file parameters via Boost PropertyTree. Reads 'TrendExtractor.config' in the current directory.
 * 
 * Usage:
 * 
 * #include "ConfigReader.hpp"
 * 
 * ConfigReader cr;
 * try {
 *  cr.init();
 *  val1 = cr.get_value("DATABASE.user");
 * } catch (Exception &e) {
 *  cout << e.what() << endl;
 * }
 */
class ConfigReader 
{
public:
	/** 
	 Initialises the ConfigReader object, must be called before other functions. 
	 @throws exception if there is an error with the config file. 
	 */
	void init();
	
	/** 
	 Retrieves a value from the config file.
	 @param p_tree_item The key of the value to retrieve.
	 @return The retrieved value.
	 @throws exception if the key does not exist.
	 */
	string get_value(string p_tree_item);
	
	/**
	 Returns a connect db string for connecting to the database.
	 @return Db connection string in the format "hostaddr=val1 connect_timeout=val2 application_name=val3 dbname=val4 user=val5 password=val6".
	 @throws exception if any keys for constructing the string does not exist.
	 */
	string get_connect_db_string();
		
private:
	boost::property_tree::ptree v_tree; /**< Boost property_tree containing content of the config file. */
	
	/**
	 Run a check on the config file to ensure all important parameters are present. This is called by the public init() function. This ensures that important  parameters that are missing are immeditately detected at the start of the application. Modify this function to ensure new key values are checked during init().
	 @throws exception if any mandatory key value is missing.
	 */
	void check_keys(); 
	
};

#endif