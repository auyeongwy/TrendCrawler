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

#ifndef _TEException_H_
#define _TEException_H_

#include <exception>
#include <string>

using namespace std;


/**
 * Custom exception class.
 *
 * Usage: 
 * 
 * #include "TEException.h"
 * 
 * try {
 *  TEException exc = new TEException("My custom error");
 *  throw exc;
 * } catch (exception &e) {
 *  cout << e.what() << endl;
 * }
 */
class TEException : public exception
{
public:
	/**
	 * Constructor.
	 * 
	 * @param p_msg String message to me returned when what() function is called.
	 */
	TEException(string p_msg);
	
	/**
	 * Overrides the base class exception's what() function.
	 * 
	 * @return String describing the exception.
	 */
	const char* what() const throw();

private:
	string v_msg; /**< String that describes the custom error. */
};


#endif