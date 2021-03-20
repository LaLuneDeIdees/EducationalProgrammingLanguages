#ifndef RUN_TIME_LDI
#define RUN_TIME_LDI

#include <iostream>
#include <dlfcn.h>
#include <fstream>
#include <vector>

#define BANKSIZE 1024*8				//smaller is fast and low memory use, but it will have bad effect
									//biger is some slow(not fact!, but in start it's true) and use many memory, but it very good
// #define CHECK_KEYS					//it delete any bad effect with hash, but it slow
#define DELTA_WHEN_CHECK_NULLS 1	//smaller is fast, but in big code i don't know how it's work
									//big code? no... I talk about many function's chains without '{lable,nums}lclr' befor caller
#define USE_CFUNCTION_HASH 		// you can use it, but it slower, when it off(not fact!)

#include "HashMap.cpp"
#include "SourceToByteCode.cpp"
#include "Jit.cpp"

using namespace std;

struct Data
{
	string data;
	uint32_t hashCode;
};
struct Library{
    string name="";
    void* library=nullptr;
};

struct CodeDequep{
	string code;
	uint16_t counter = 0;
	CodeDequep(string s){
		code=s;
		counter=0;
	}
};
vector<CodeDequep>ByteCodeDequep;
vector<Data> Stack;
HashMap<uint32_t> Labels;			   	//save pointer to stack
//HashMap<Data> MemorazeFunctionResults;  //key is to_string(hashC(a))+to_string(hashC(b))+to_string(hashC(func))
HashMap<Library> CLibrary;

#ifdef USE_CFUNCTION_HASH
	HashMap<void(*)(vector<Data>&)> CFunction;
#endif

uint32_t MonadeCounter = 0;


uint8_t nextByte(){
	// uint8_t out =  *(ByteCodeDequep.back().begin());
	// ByteCodeDequep.back().erase(ByteCodeDequep.back().begin());
	uint8_t out =  ByteCodeDequep.back().code[ByteCodeDequep.back().counter++];
	return out;
}
string nextSection(){
	// string out="";
	// uint8_t byte = nextByte();
	// while(byte!=CODE_END_SECTION){
	// 	out+=byte;

	// 	byte = nextByte();
	// }
	uint16_t n = ByteCodeDequep.back().code.find('\x01',ByteCodeDequep.back().counter)-ByteCodeDequep.back().counter;
	string out = ByteCodeDequep.back().code.substr(ByteCodeDequep.back().counter,n);
	ByteCodeDequep.back().counter+=n+1;
	return out;
}
uint32_t nextSectionAsHash(){
	uint32_t out=0;
	uint8_t byte;
	for(int i=0;i<4;i++){
		byte = nextByte();
		out|=byte<<(i*8);
	}
	nextByte();
	return out;
}
void checkSize(){
	static uint32_t lastn = 0;
	if(abs((int32_t)(ByteCodeDequep.size()-lastn))>DELTA_WHEN_CHECK_NULLS){
		lastn = ByteCodeDequep.size();
		for(uint32_t i=0;i<lastn;i++){
			// if(ByteCodeDequep[i].size()<=0){
			if(ByteCodeDequep[i].counter>=ByteCodeDequep[i].code.size()){
				ByteCodeDequep.erase(ByteCodeDequep.begin()+i);
				lastn--;i--;
			}
		}
	}
}
void run(){
	string name = "";
	uint32_t hashCode;
	Data n;
	while(ByteCodeDequep.size()>0){
		// if(ByteCodeDequep.back().size()<=0){ByteCodeDequep.pop_back();continue;}
		if(ByteCodeDequep.back().counter>=ByteCodeDequep.back().code.size()){ByteCodeDequep.pop_back();continue;}

		checkSize();
		uint8_t byte = nextByte();

		switch (byte)
		{
		case CODE_REGISTER_LABEL:
			name = nextSection();
			Labels.put(name,Stack.size(),nextSectionAsHash());
			break;
		case CODE_REGISTER_DATA:
			n.data = nextSection();
			n.hashCode = nextSectionAsHash();
			Stack.push_back(n);
			break;
		case CODE_DECREMENT_LABEL:
			Labels.datas.back().data-= 1;
			break;
		case CODE_DATA_FROM_LABEL_TO_STACK:
			name = nextSection();
			Stack.push_back(Stack[Labels.getLast(name,nextSectionAsHash())]);
			break;
		case CODE_MONAD:
			n.data = to_string(MonadeCounter++);
			n.hashCode = hashC(n.data);
			Stack.push_back(n);
			break;
		case CODE_LLIB:
			name = Stack.back().data;
			hashCode = Stack.back().hashCode;
			Stack.pop_back();
			if(1){
				ifstream input(name);
				if(!input.is_open()){cout <<"\n\nERROR: can't open file on load lundi module: "<<name<<"\n\n";}
				else{
					string line="",tmp;
					while (!input.eof())
					{
						getline(input,tmp);
						tmp+='\n';
						line+=tmp;
					}
					input.close();
					ByteCodeDequep.push_back(SourceToByteCode(line).bytes);
				}
			}
			break;
		case CODE_EVAL:
			name = Stack.back().data;
			hashCode = Stack.back().hashCode;
			Stack.pop_back();
			ByteCodeDequep.push_back(SourceToByteCode(name,hashCode).bytes);
			break;
		case CODE_LCLR:
			name = Stack.back().data;Stack.pop_back();
			if(1){
				int idx = name.find('|');
				string startLabel = name.substr(0,idx);

				uint32_t lastIdx = Labels.getLast(startLabel);

				int numSave = stoi(name.substr(idx+1));
				vector<Data> saves;
				for(int i=0;i<numSave;i++){
					saves.push_back(Stack.back());
					Stack.pop_back();
				}

				while (Labels.datas.back().key!=startLabel)
				{
					Labels.pop();
				}
				Labels.pop();

				while (Stack.size()>lastIdx)
				{
					Stack.pop_back();
				}
				
				
				

				for(int i=0;i<numSave;i++){
					Stack.push_back(saves.back());
					saves.pop_back();
				}

			}
			break;
		case CODE_CLIB:
			name = Stack.back().data;Stack.pop_back();
			if(1){
				Library l;
				l.name = name;
				if(l.name.find('/')!=-1){
					l.name = l.name.substr(l.name.find_last_of('/')+1);
				}
				name+=".so";

				Library already = CLibrary.getLast(l.name);
				if(!CLibrary.fail){
					n.data=l.name;
					n.hashCode = hashC(l.name);
					Stack.push_back(n);
					break;
				}

				l.library = dlopen(name.c_str(),RTLD_LAZY);
				if(l.library==nullptr){
					cout << "ERROR: can't load C/C++ dinamic Library: " << name<<endl;
					break;
				}
				CLibrary.put(l.name,l);

				n.data=l.name;
				n.hashCode = hashC(l.name);
				Stack.push_back(n);
			}
			break;
		case CODE_CALL_CLIB:
			if(1){
				name = nextSection();//library
				hashCode = nextSectionAsHash();
				string name1 = nextSection(); //function
				uint32_t hashCode1 = nextSectionAsHash();

				void (*ff)(vector<Data>&);
				#ifdef USE_CFUNCTION_HASH
					ff = CFunction.getLast("",hashCode+hashCode1);
					if(!CFunction.fail){
						ff(Stack);
						break;
					}
				#endif

				Library l = CLibrary.getLast(name,hashCode);
				if(CLibrary.fail){
					cout << "ERROR: C/C++ dinamic library not loaded: "<<name<<endl;
					break;
				}

				
				ff = (void(*)(vector<Data>&))dlsym(l.library,name1.c_str());
				if(ff==nullptr){
					cout << "ERROR: can't call function: \""<<name1<<"\"  from C/C++ dinamic library:"<<l.name<<endl;
					break;
				}
				#ifdef USE_CFUNCTION_HASH
					CFunction.put("",ff,hashCode+hashCode1);
				#endif
				ff(Stack);
			}
			break;
		default:
			cout << "UNSUPPORTED_STATE:=: "<<int(byte)<<endl;
			break;
		}
	}
}

int RunTime(int argc,char** arga){
	if(argc==2 && string(arga[1])=="cmd"){
		while(true){
			string line;
			getline(cin,line);
			line+='\n';
			ByteCodeDequep.push_back(SourceToByteCode(line).bytes);
			run();
			cout <<"STACK:";
			for(auto i:Stack){
				cout << '\t'<<i.data << endl;
			}
		}
	}else if(argc==3 && string(arga[1])=="runf"){
		ifstream code(arga[2]);
		if(!code.is_open()){
			cout<<"ERROR: can't open file: "<<arga[2]<<endl<<endl;
			return 1;
		}
		string line = "";
		string tmp ="";
		while (!code.eof())
		{
			getline(code,tmp);
			tmp+='\n';
			line+=tmp;
		}
		ByteCodeDequep.push_back(SourceToByteCode(line).bytes);
		run();
	}else if(argc==3 && string(arga[1])=="runb"){
		ifstream code(arga[2]);
		if(!code.is_open()){
			cout<<"ERROR: can't open file: "<<arga[2]<<endl<<endl;
			return 1;
		}
		string line = "";
		string tmp ="";
		while (!code.eof())
		{
			getline(code,tmp);
			line+=tmp;
		}
		ByteCodeDequep.push_back(line);
		run();
	}else if(argc==4 && string(arga[1])=="bin"){
		ifstream code(arga[2]);
		if(!code.is_open()){
			cout<<"ERROR: can't open file: "<<arga[2]<<endl<<endl;
			return 1;
		}
		string line = "";
		string tmp ="";
		while (!code.eof())
		{
			getline(code,tmp);
			tmp+='\n';
			line+=tmp;
		}
		ofstream bin(arga[3]);
		bin << SourceToByteCode(line).bytes;
	}else{
		cout <<"use:\n\
	{run} cmd - interpriter\n\
	{run} runf $file - run from source code\n\
	{run} bin $file $outputfile - from source to bytecode\n\
	{run} runb $file - run from bytecode\n\
\n";
	}

	// cout <<"STACK:";
	// for(auto i:Stack){
	// 	cout << '\t'<<i.data << endl;
	// }

	return 0;
}

#endif