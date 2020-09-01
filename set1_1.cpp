#include <iostream>
#include <string>
#include <sstream>
#include <bitset>


int main()
{
	int i,j;  // for iteration
	int l = 0; //how many times does the while loop run
	std::string charc,newStr;


	std::string hexToBinary = "";
	std::string ref = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	std::string hex1;
	std::string base64="";

	//getting the hexcode 
	std::cin >> hex1;
	
	//Number of characters  
	int bytes = hex1.size();

	//Conversion of the given hex data to binary
	for(i=0;i<bytes;i++)
	{

		
	newStr = hex1[i];

	//conversion of string into int
	int con_int_hex = std::stoi(newStr,nullptr,16);
	//conversion into binary
    std::string binary = std::bitset<4>(con_int_hex).to_string(); 
	//joining all hex data together
	hexToBinary = hexToBinary + binary;
	
	}


	int bytes1 = hexToBinary.size();
	
	//Conversion to base 64
	for(j=0;j<bytes1;j=j+6)
	{	//Taking only 6 binary digits at a time
		std::string only6 = hexToBinary.substr(j,6);
		
		//Adding 00 for encoding for last digits
	 	if (only6.size()!= 0)
		{
			while(only6.size()!=6)
			{ 
			only6= only6 + "0";
		  	l = l+1;
			}
		}
		//string to int
		int con_int_base64 = std::stoi(only6,nullptr,2);

		//assigning base64 values
		std::string sextets = ref.substr(con_int_base64,1);
		base64 = base64 + sextets ;
	}
//for padding
if(l==2)
{
	base64=base64 + "=";
	}
else if (l == 4)
{
	base64 = base64 + "==";
	}

std::cout << base64<< std::endl;
 
return 0;
}
