#include <iostream>
#include <string>
#include <sstream>
#include <bitset>

//Hexadecimal to Binary Conversion

std::string hex_Binary (std::string hex1)
	{
	int i;  // for iteration
	

	std::string hexToBinary = "";
	std::string newStr;
	
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
	return(hexToBinary);
}
int main()
{
	std::string first,second;
	long int con_int_hex1;
	long int con_int_hex2;
	long int binary_hex2;
	char c;

	std::string str1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	std::cout << "Enter The Hex" << std::endl;
	std::cin >> first;
	std::string binary_hex1 = hex_Binary (first);

	for(int j=0;j < str1.size();j++)
	{
			c = str1[j];
	
			binary_hex2 = int(c);
	
	
    		for(int i=0;i<binary_hex1.size();i = i+8)
				{		
					std::string str1 = binary_hex1.substr(i,8);
		

					con_int_hex1 = std::stoi(str1,nullptr,2);
		
					int final_ans = con_int_hex1^binary_hex2;
					//std::string final1 = str1[final_ans];
					std::cout << char(final_ans);
					

				}
		std::cout << std::endl;
		
	}

return 0;
}
