#include <iostream>
#include <string>
#include <sstream>
#include <bitset>

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

	std::cout << "Enter The second Hex" << std::endl;
	std::cin >> first;
	std::cout << "Enter The second Hex" << std::endl;
	std::cin >> second;
	std::string binary_hex1 = hex_Binary (first);
	std::string binary_hex2 = hex_Binary (second);

    for(int i=0;i<binary_hex1.size();i = i+4)
	{	
		std::string str1 = binary_hex1.substr(i,4);
		std::string str2 = binary_hex2.substr(i,4);

		con_int_hex1 = std::stoi(str1,nullptr,2);
		con_int_hex2 = std::stoi(str2,nullptr,2);
		long int final_ans = con_int_hex1^con_int_hex2;
		std::cout << std::hex << final_ans;
	}


return 0;
