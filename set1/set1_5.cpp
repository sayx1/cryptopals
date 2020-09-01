#include <iostream>
#include <string>

int main(){
	std::string data="Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal";
	std::string key="ICE";
	for(int i=0;i<data.size();i=i+3)
	{	/*
		char a,b,c;
		int a1,b1,c1;
		a = data[i];
		b = data[i+1];
		c = data[i+
		a1 = key[0]
		*/
		int encrypted1 = data[i]^key[0];
		int encrypted2 = data[i+1]^key[1];
		int encrypted3 = data[i+2]^key[2];
		std::cout << std::hex << encrypted1 << encrypted2 << encrypted3;

	}

return 0;
	}
