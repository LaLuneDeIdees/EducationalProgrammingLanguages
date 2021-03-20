#include <iostream>
#include <fstream>
#include <sstream>
#include "parser.cpp"

using namespace std;

int main(int argc, char** args){
	if(argc<3){
		cout << "we need 2 arguments:\n"
				 << "\t1 - input file\n"
				 << "\t2 - output file\n";
				 return 1;
	}
	ifstream codeinput(args[1]);
	ofstream cppout(args[2]);
	
	cout << "\n"
			 << "file: " << args[1] << " is " 
			 << ((codeinput.is_open())? "open":"can't open")
			 << "\nfile: " << args[2] << " is " 
			 << ((codeinput.is_open())? "open":"can't open")
			 << "\n";
				 
	if(!(codeinput.is_open() & codeinput.is_open())){
				 return 1;
	}
	string code,tmp;
	while(!codeinput.eof()){
		getline(codeinput, tmp);
		code+=tmp+'\n';
	}
	parse(&code);
	
	cppout << "\n####################################################\n"
				 << code;
	return 0;
}
